import os
import json
import asyncio
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Canonical Writing Model (domain-specific knowledge, loaded as DATA)
# ---------------------------------------------------------------------------
def load_canonical_writing_model() -> dict:
    path = ROOT_DIR / "canonical_writing_model.json"
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        logger.warning(f"Could not load canonical writing model: {e}")
        return {"domains": []}


CANONICAL_WRITING_MODEL = load_canonical_writing_model()
CANONICAL_DOMAIN_NAMES = [d.get("domain_name") for d in CANONICAL_WRITING_MODEL.get("domains", [])]
_DOMAINS_BY_NAME = {d.get("domain_name"): d for d in CANONICAL_WRITING_MODEL.get("domains", [])}


def _build_compact_domain_index() -> list:
    """STAGE A — a tiny index used only to SELECT relevant domains.
    Per domain: name + one-sentence communicative function + relationships.
    The full structured records stay on disk in canonical_writing_model.json."""
    index = []
    for d in CANONICAL_WRITING_MODEL.get("domains", []):
        fns = d.get("communicative_functions", [])
        one_sentence = ("Serves to " + ", ".join(fns[:3]) + ".") if fns else ""
        index.append({
            "domain_name": d.get("domain_name"),
            "communicative_function": one_sentence,
            "relationships": d.get("relationships_to_other_domains", []),
        })
    return index


COMPACT_DOMAIN_INDEX = _build_compact_domain_index()


def get_relevant_domain_data(domain_names: List[str]) -> list:
    """STAGE B — retrieve COMPLETE domain records by exact domain name.
    Single source of truth; the canonical model is not duplicated in code."""
    seen, out = set(), []
    for name in domain_names or []:
        rec = _DOMAINS_BY_NAME.get(name)
        if rec and name not in seen:
            seen.add(name)
            out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Telos(BaseModel):
    """A — Current Developmental Telos (provisional, revisable)."""
    governing_pedagogical_purpose: str = ""
    immediate_task_purpose: str = ""
    teacher_intentions: str = ""
    assignment_context: str = ""
    audience_or_communicative_purpose: str = ""
    unresolved_ambiguity: str = ""
    telos_changed: str = ""


class DevelopmentalTheory(BaseModel):
    """C — Working Developmental Theory (one evolving, provisional theory)."""
    current_telos: str = ""
    current_organization: str = ""
    observed_differentiations: List[str] = Field(default_factory=list)
    observed_integrations: List[str] = Field(default_factory=list)
    observed_coordinations: List[str] = Field(default_factory=list)
    emerging_intentional_control: str = ""
    unresolved_tensions: List[str] = Field(default_factory=list)
    cultural_resources_in_use: List[str] = Field(default_factory=list)
    potential_cultural_resources: List[str] = Field(default_factory=list)
    possible_reorganizations: List[str] = Field(default_factory=list)
    current_uncertainty: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    complicating_evidence: List[str] = Field(default_factory=list)
    currently_relevant_domains: List[str] = Field(default_factory=list)
    changes_since_previous: str = ""


class CandidateInvitation(BaseModel):
    """D — one candidate developmental invitation."""
    invitation: str = ""
    developmental_possibility: str = ""
    coherence_with_telos: str = ""
    intended_participation: str = ""
    what_ai_could_learn: str = ""
    uncertainty_or_risk: str = ""


class SelectedInvitation(BaseModel):
    """E — selected developmental invitation."""
    invitation: str = ""
    selection_basis: str = ""


class Turn(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # "student" or "ai"
    kind: str = "message"
    content: str
    created_at: str = Field(default_factory=now_iso)


class InteractionRecord(BaseModel):
    """B — a meaningful participation event + the reasoning it produced."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_kind: str = ""
    student_content: str = ""
    candidate_invitations: List[CandidateInvitation] = Field(default_factory=list)
    selected_invitation: SelectedInvitation = Field(default_factory=SelectedInvitation)
    observed_reorganization: str = ""
    created_at: str = Field(default_factory=now_iso)


class TheorySnapshot(BaseModel):
    version: int
    telos: Telos
    theory: DevelopmentalTheory
    created_at: str = Field(default_factory=now_iso)


class SessionCreate(BaseModel):
    assignment: str
    pedagogical_purpose: str
    current_writing_task: str
    teacher_notes: Optional[str] = ""


class TelosEdit(BaseModel):
    assignment: Optional[str] = None
    pedagogical_purpose: Optional[str] = None
    current_writing_task: Optional[str] = None
    teacher_notes: Optional[str] = None
    note: Optional[str] = ""


class InteractRequest(BaseModel):
    content: str
    kind: str = "writing"  # writing | revise | continue | answer | explain


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assignment: str
    pedagogical_purpose: str
    current_writing_task: str
    teacher_notes: Optional[str] = ""
    turns: List[Turn] = Field(default_factory=list)
    telos: Telos = Field(default_factory=Telos)
    theory: DevelopmentalTheory = Field(default_factory=DevelopmentalTheory)
    theory_history: List[TheorySnapshot] = Field(default_factory=list)
    interactions: List[InteractionRecord] = Field(default_factory=list)
    teacher_edits: List[dict] = Field(default_factory=list)
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)


# ---------------------------------------------------------------------------
# Developmental Guide Engine
# ---------------------------------------------------------------------------
SYSTEM_MESSAGE = """You are a developmental pedagogical guide. Interpret the student's participation as an unfolding process organized relative to a provisional developmental telos.

Do not diagnose hidden traits, abilities, competencies, or stages. Do not assume a universal developmental sequence. Do not assign stages, levels, scores, or stable learner characteristics. Do not posit hidden psychological entities behind observable activity. Attend to observable changes in differentiation, integration, coordination, hierarchical organization, flexibility, intentionality, and participation, visible in writing, revision, explanation, choice, hesitation, response, and participation over time.

Maintain ONE provisional working theory of the developing pedagogical SYSTEM, including the student, teacher intentions, task, telos, cultural resources, prior interaction, current activity, and uncertainty — not merely a profile of the student. Treat all interpretations as provisional. Never treat one successful response as evidence of a stable competence.

Guidance is functionally asymmetric: you temporarily take responsibility for guiding participation within the teacher's purposes and constraints. The student must remain the author of the work — NEVER write or substantially rewrite the student's text, never produce a model passage for them to copy, never give the answer.

You are domain-independent as a REASONER. You hold NO built-in instructional sequence for essay writing. Domain-specific writing knowledge comes ONLY from the CANONICAL WRITING MODEL supplied in the request. Keep the two forms of knowledge distinct: (1) developmental reasoning (this engine, domain-independent) and (2) canonical writing knowledge (structured cultural resources you consult). Do not collapse them.

CANONICAL WRITING MODEL — the supplied domains describe culturally established FUNCTIONS of effective writing and cultural RESOURCES for interpreting student writing. They are NOT developmental stages, NOT a required sequence, NOT rigid templates. Never force the student through the domains in a predetermined order. Determine which domains are currently RELEVANT based on teacher purpose, student purpose, assignment, audience, genre, current writing, and interaction history. Use canonical resources to EXTEND the student's present organization, never to replace it.

INSIDE-OUTSIDE COORDINATION RULE — never impose canonical structures before understanding the student's developing organization. For every interaction determine: (1) What is the student trying to accomplish? (2) What does the assignment require? (3) What does the reader need? (4) Which canonical writing domains are currently relevant? (5) How can canonical resources extend the student's present organization rather than replace it? Development proceeds by COORDINATING the student's emerging organization, the teacher's purposes, the assignment, the reader's needs, and the culturally established organization of writing.

DRAFT RULE: When the input is a draft ("writing", "revise", or "continue") it is the student's full, authoritative current text. If it differs from their previous draft, they HAVE revised — name the change you see and build on it. Never claim a student has not revised when their new draft differs from the old one.

RECURSIVE LOOP — after every interaction:
1. State the current telos.
2. Describe current organization relative to the telos.
3. Identify observed differentiation, integration, coordination, or tension.
4. Identify evidence supporting AND evidence complicating the interpretation.
5. Describe what appears to have changed since the previous interaction.
6. Identify possible developmental reorganizations.
7. Generate TWO or THREE candidate developmental invitations.
8. Select ONE invitation because it is sufficiently coherent (with telos, participation, organization, history, teacher intentions, and uncertainty) — NOT because it is optimal or objectively best. If several remain equally coherent, pick one without inventing a false distinction.
9. Produce ONE concise student-facing invitation.
10. Preserve uncertainty and REVISE the full working theory (do not merely append a note).

STUDENT-FACING INVITATION RULES: The student sees only ONE concise invitation. It should acknowledge something meaningful in the student's participation, connect to the current purpose, and ask the student to perform the next intellectual or writing action. Avoid long analyses, grading language, evidence-free praise, lists of multiple problems, rewriting, giving the answer, naming a developmental level, or saying the student "lacks" a trait or skill.

OUTPUT FORMAT — respond with ONLY a valid JSON object, no markdown fences, no prose outside it:
{
  "student_facing_invitation": "one concise invitation shown to the student (equals selected_invitation.invitation)",
  "telos": {
    "governing_pedagogical_purpose": "", "immediate_task_purpose": "", "teacher_intentions": "",
    "assignment_context": "", "audience_or_communicative_purpose": "", "unresolved_ambiguity": "",
    "telos_changed": "describe if/how the telos shifted this turn, else 'no change'"
  },
  "theory": {
    "current_telos": "", "current_organization": "",
    "observed_differentiations": [], "observed_integrations": [], "observed_coordinations": [],
    "emerging_intentional_control": "",
    "unresolved_tensions": [], "cultural_resources_in_use": [], "potential_cultural_resources": [],
    "possible_reorganizations": [], "current_uncertainty": [],
    "supporting_evidence": [], "complicating_evidence": [],
    "currently_relevant_domains": ["names of the canonical domains currently relevant, chosen from the supplied model — not a fixed order"],
    "changes_since_previous": "what changed vs the prior theory (or 'initial' on first turn)"
  },
  "candidate_invitations": [
    {"invitation": "", "developmental_possibility": "", "coherence_with_telos": "",
     "intended_participation": "", "what_ai_could_learn": "", "uncertainty_or_risk": ""}
  ],
  "selected_invitation": {"invitation": "", "selection_basis": "coherence-based, not optimality"},
  "observed_reorganization": "how the student's participation actually reorganized this turn (or 'initial' on first turn)"
}
Provide 2 or 3 candidate_invitations. Do not store numeric scores anywhere.

BREVITY (critical — the response must complete quickly): Be terse in ALL internal fields. Each string field is a short phrase or one short sentence. Each list holds at most 2-3 brief items. Prefer 2 candidate invitations (add a 3rd only if genuinely distinct); keep each candidate's fields to short phrases and its invitation to one sentence. The student_facing_invitation is 2-4 sentences. Do not repeat content across fields. Do not pad. Output compact JSON."""

DRAFT_KINDS = {"writing", "revise", "continue"}


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1] if "```" in text else text
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


def _compact_theory(theory: DevelopmentalTheory) -> dict:
    """Compact projection of the working theory for the per-turn prompt
    (full theory + prior snapshots are still persisted in the DB)."""
    return {
        "current_telos": theory.current_telos,
        "current_organization": theory.current_organization,
        "unresolved_tensions": theory.unresolved_tensions,
        "currently_relevant_domains": theory.currently_relevant_domains,
        "current_uncertainty": theory.current_uncertainty,
        "complicating_evidence": theory.complicating_evidence,
        "changes_since_previous": theory.changes_since_previous,
    }


def _previous_draft(session: Session) -> Optional[str]:
    prior_turns = session.turns[:-1] if session.turns else []
    for t in reversed(prior_turns):
        if t.role == "student" and t.kind in DRAFT_KINDS:
            return t.content
    return None


def _latest_block(session: Session, req: InteractRequest) -> str:
    if req.kind in DRAFT_KINDS:
        prev = _previous_draft(session)
        return f"""STUDENT'S CURRENT DRAFT (full authoritative current text; kind = "{req.kind}"):
{req.content}

PREVIOUS DRAFT:
{prev if prev else "(none — first draft)"}

Compare the CURRENT DRAFT to the PREVIOUS DRAFT literally. If they differ, the student HAS revised — acknowledge the specific change. Never claim otherwise."""
    return f"""STUDENT'S LATEST RESPONSE (a reply to your last invitation, NOT a new draft; kind = "{req.kind}"):
{req.content}"""


def _interaction_summary(session: Session) -> str:
    lines = [
        f"- turn {i + 1} ({ir.student_kind}): {ir.observed_reorganization}"
        for i, ir in enumerate(session.interactions)
        if ir.observed_reorganization
    ]
    return "\n".join(lines) if lines else "(no prior turns)"


def _selector_prompt(session: Session, req: InteractRequest) -> str:
    prior = [d for d in session.theory.currently_relevant_domains if d]
    return f"""You choose which canonical writing domains are relevant to the student's CURRENT participation. Do NOT force a sequence. Choose the 1-2 most relevant domains, plus at most ONE closely related domain only if needed to interpret the relationship among parts. Reassess freely — do not mechanically keep prior domains if the writing/tension has changed.

TELOS: {session.telos.governing_pedagogical_purpose} | task: {session.telos.immediate_task_purpose}
DOMAINS PREVIOUSLY RELEVANT: {prior if prior else "(none yet)"}

COMPACT DOMAIN INDEX:
{json.dumps(COMPACT_DOMAIN_INDEX, indent=2)}

{_latest_block(session, req)}

Respond with ONLY this JSON: {{"relevant_domains": ["exact domain name", "..."]}} (1 to 3 names, exact strings from the index)."""


def _build_prompt(session: Session, req: InteractRequest, relevant_domains: List[str]) -> str:
    full_domain_data = get_relevant_domain_data(relevant_domains)
    return f"""CURRENT DEVELOPMENTAL TELOS (component A — provisional, revisable):
{json.dumps(session.telos.model_dump(), indent=2)}

COMPACT CURRENT DEVELOPMENTAL THEORY (component C — your evolving theory so far):
{json.dumps(_compact_theory(session.theory), indent=2)}

INTERACTION SUMMARY (component B — concise history of how participation reorganized):
{_interaction_summary(session)}

CURRENTLY RELEVANT CANONICAL DOMAINS (selected for THIS turn): {relevant_domains}

FULL DATA FOR THE RELEVANT CANONICAL DOMAINS ONLY (domain-specific cultural resources loaded as DATA — use these, do not rely on general writing knowledge; you may adjust which domains are relevant and reflect that in currently_relevant_domains):
{json.dumps(full_domain_data, indent=2)}

{_latest_block(session, req)}

Run the full recursive loop and respond with ONLY the JSON object described in your instructions. Revise the ENTIRE working theory rather than appending a note. Keep every field terse per the BREVITY rule."""


def _parse_engine_output(session: Session, raw: str) -> dict:
    try:
        data = _extract_json(raw)
        telos = Telos(**{**session.telos.model_dump(), **data.get("telos", {})})
        theory = DevelopmentalTheory(**{**session.theory.model_dump(), **data.get("theory", {})})
        candidates = [CandidateInvitation(**c) for c in data.get("candidate_invitations", [])]
        selected = SelectedInvitation(**data.get("selected_invitation", {}))
        invitation = (data.get("student_facing_invitation") or selected.invitation or "").strip()
        observed_reorg = data.get("observed_reorganization", "").strip()
    except Exception as e:  # noqa: BLE001
        logger.error(f"Engine parse error: {e}; raw={raw[:800]}")
        raise ValueError("The developmental engine returned an unreadable response.")

    if not invitation:
        raise ValueError("The developmental engine did not return an invitation.")
    if not selected.invitation:
        selected.invitation = invitation

    return {
        "invitation": invitation,
        "telos": telos,
        "theory": theory,
        "candidates": candidates,
        "selected": selected,
        "observed_reorganization": observed_reorg,
    }


def _apply_engine_result(session: Session, req: InteractRequest, result: dict) -> None:
    # snapshot the theory that motivated this response BEFORE replacing it
    session.theory_history.append(
        TheorySnapshot(
            version=len(session.theory_history) + 1,
            telos=session.telos,
            theory=session.theory,
        )
    )
    session.turns.append(Turn(role="ai", kind="invitation", content=result["invitation"]))
    session.telos = result["telos"]
    session.theory = result["theory"]
    session.interactions.append(
        InteractionRecord(
            student_kind=req.kind,
            student_content=req.content.strip(),
            candidate_invitations=result["candidates"],
            selected_invitation=result["selected"],
            observed_reorganization=result["observed_reorganization"],
        )
    )
    session.updated_at = now_iso()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"message": "Developmental Guide Engine"}


@api_router.post("/sessions", response_model=Session)
async def create_session(payload: SessionCreate):
    telos = Telos(
        governing_pedagogical_purpose=payload.pedagogical_purpose,
        immediate_task_purpose=payload.current_writing_task,
        teacher_intentions=payload.teacher_notes or "",
        assignment_context=payload.assignment,
    )
    session = Session(**payload.model_dump(), telos=telos)
    await db.sessions.insert_one(session.model_dump())
    return session


@api_router.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    doc = await db.sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    return Session(**doc)


@api_router.patch("/sessions/{session_id}/telos", response_model=Session)
async def edit_telos(session_id: str, edit: TelosEdit):
    doc = await db.sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    session = Session(**doc)

    changes = {}
    for field in ("assignment", "pedagogical_purpose", "current_writing_task", "teacher_notes"):
        val = getattr(edit, field)
        if val is not None and val != getattr(session, field):
            changes[field] = {"from": getattr(session, field), "to": val}
            setattr(session, field, val)

    if not changes:
        return session

    # reflect edits into the current telos
    session.telos.governing_pedagogical_purpose = session.pedagogical_purpose
    session.telos.immediate_task_purpose = session.current_writing_task
    session.telos.assignment_context = session.assignment
    session.telos.teacher_intentions = session.teacher_notes or ""
    session.telos.telos_changed = "Teacher revised the telos."

    session.teacher_edits.append({
        "id": str(uuid.uuid4()),
        "changes": changes,
        "note": edit.note or "",
        "created_at": now_iso(),
    })
    session.updated_at = now_iso()

    await db.sessions.update_one(
        {"id": session_id},
        {"$set": {
            "assignment": session.assignment,
            "pedagogical_purpose": session.pedagogical_purpose,
            "current_writing_task": session.current_writing_task,
            "teacher_notes": session.teacher_notes,
            "telos": session.telos.model_dump(),
            "teacher_edits": session.teacher_edits,
            "updated_at": session.updated_at,
        }},
    )
    return session


async def _select_relevant_domains(session: Session, req: InteractRequest) -> List[str]:
    """STAGE A — pick the 1-3 canonical domains relevant to this turn using the
    compact index only. Retries once on transient failure, then falls back to the
    theory's prior relevant domains (or Whole Essay Purpose)."""
    prompt = _selector_prompt(session, req)
    for attempt in range(2):
        try:
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"select-{session.id}",
                system_message="You select relevant canonical writing domains. Respond with ONLY the requested JSON.",
            ).with_model("anthropic", "claude-sonnet-4-6")
            raw = await chat.send_message(UserMessage(text=prompt))
            names = [n for n in _extract_json(raw).get("relevant_domains", []) if n in _DOMAINS_BY_NAME]
            if names:
                return names[:3]
        except Exception as e:  # noqa: BLE001
            logger.warning(f"domain selection attempt {attempt + 1} failed: {e}")
            if attempt == 0:
                await asyncio.sleep(3)
    prior = [n for n in session.theory.currently_relevant_domains if n in _DOMAINS_BY_NAME]
    return prior[:2] if prior else ["Whole Essay Purpose"]


@api_router.post("/sessions/{session_id}/interact")
async def interact(session_id: str, req: InteractRequest):
    doc = await db.sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    session = Session(**doc)

    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Empty submission")

    session.turns.append(Turn(role="student", kind=req.kind, content=req.content.strip()))

    async def event_generator():
        try:
            # STAGE A: choose relevant domains from the compact index
            relevant = await _select_relevant_domains(session, req)
            # STAGE B: reason with full data for only those domains
            prompt = _build_prompt(session, req, relevant)
            logger.info(f"[interact] turn domains={relevant} reasoner_prompt_bytes={len(prompt)}")

            result = None
            last_err = None
            for attempt in range(2):  # one retry on transient/unreadable failure
                raw_parts: List[str] = []
                try:
                    chat = LlmChat(
                        api_key=EMERGENT_LLM_KEY,
                        session_id=f"dev-{session.id}",
                        system_message=SYSTEM_MESSAGE,
                    ).with_model("anthropic", "claude-sonnet-4-6")
                    async for ev in chat.stream_message(UserMessage(text=prompt)):
                        if isinstance(ev, TextDelta):
                            raw_parts.append(ev.content)
                            yield ": tick\n\n"  # heartbeat keeps the connection warm
                        elif isinstance(ev, StreamDone):
                            break
                    result = _parse_engine_output(session, "".join(raw_parts))
                    break
                except Exception as e:  # noqa: BLE001
                    last_err = e
                    logger.warning(f"reasoner attempt {attempt + 1} failed: {e}")
                    if attempt == 0:
                        yield ": retry\n\n"
                        await asyncio.sleep(3)
            if result is None:
                raise last_err or RuntimeError("engine failed")

            _apply_engine_result(session, req, result)
            await db.sessions.update_one(
                {"id": session_id},
                {"$set": {
                    "turns": [t.model_dump() for t in session.turns],
                    "telos": session.telos.model_dump(),
                    "theory": session.theory.model_dump(),
                    "theory_history": [s.model_dump() for s in session.theory_history],
                    "interactions": [i.model_dump() for i in session.interactions],
                    "updated_at": session.updated_at,
                }},
            )
            yield f"event: done\ndata: {json.dumps(session.model_dump())}\n\n"
        except Exception as e:  # noqa: BLE001
            logger.error(f"interact stream error: {e}")
            yield f"event: error\ndata: {json.dumps({'detail': 'The developmental engine could not respond. Please try again.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
