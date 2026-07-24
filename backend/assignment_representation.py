"""
Compass 2.0 — Sprint 1: Assignment Representation.

A self-contained vertical slice. Compass helps the student build an adequate
REPRESENTATION of what an assignment requires before any knowledge gathering or
writing. It leads with assignment demands, uses the student's words diagnostically,
scaffolds ONE high-leverage demand at a time, and never writes the response.

This module owns its own APIRouter + Mongo collection (`assignment_sessions`) and
reuses the shared LLM client + helpers from server.py. It does NOT touch the
existing Milestone writing engine or the Meaning Workspace.
"""
import json
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from emergentintegrations.llm.chat import LlmChat, UserMessage

router = APIRouter(prefix="/api/assignment", tags=["assignment-representation"])

# Injected by server.py at import time to avoid duplicate Mongo clients / circular imports.
_db = None
_llm_key = None
_now_iso = None


def init(db, llm_key, now_iso):
    global _db, _llm_key, _now_iso
    _db = db
    _llm_key = llm_key
    _now_iso = now_iso


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
class AssignmentDemand(BaseModel):
    id: str = Field(default_factory=lambda: f"dem_{uuid.uuid4()}")
    label: str
    description: str = ""
    source: str = "explicit"                 # explicit | inferred
    supporting_wording: str = ""             # exact quote from the assignment (explicit) or "" (inferred)
    operation: str = ""                      # developmental operation: Differentiate, Compare, Define, Explain, Exemplify, Relate, Analyze...
    concepts: List[str] = Field(default_factory=list)
    status: str = "unconfirmed"              # understood | developing | needs_attention | unconfirmed
    importance: str = "essential"            # essential | supporting
    learner_evidence: str = ""
    confidence: float = 0.0                  # INTERNAL ONLY — never exposed in the UI
    derivable_from_assignment: bool = True   # is the needed understanding discoverable from the assignment text itself?
    scaffold_level: int = 0
    scaffold_attempts: int = 0


class Scaffold(BaseModel):
    demand_id: str = ""
    level: int = 1                           # 0 independent · 1 attention cue · 2 guided construction · 3 direct teaching
    instructionType: str = ""                # independent | attention_cue | guided_construction | direct_teaching
    targetOperation: str = ""
    concepts: List[str] = Field(default_factory=list)
    relevant_wording: str = ""               # the assignment wording this scaffold points at
    studentTask: str = ""                    # what the student must DO (performs the operation)
    expectedEvidence: str = ""               # what a successful performance looks like
    nextIfSuccessful: str = ""
    nextIfUnsuccessful: str = ""
    requires_reconstruction: bool = False    # level 3: learner must reconstruct the concept in their own words


class InteractionRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"int_{uuid.uuid4()}")
    kind: str                                # interpretation | operation | restatement
    student_text: str = ""
    target_demand_id: str = ""
    scaffold: dict = Field(default_factory=dict)   # snapshot of the scaffold the student was responding to
    evaluation: dict = Field(default_factory=dict)
    created_at: str = ""


class AssignmentSession(BaseModel):
    id: str = Field(default_factory=lambda: f"asg_{uuid.uuid4()}")
    assignment_text: str
    demands: List[AssignmentDemand] = Field(default_factory=list)
    important_distinctions: List[str] = Field(default_factory=list)   # AI analysis: key distinctions the task hinges on
    ambiguities: List[str] = Field(default_factory=list)              # AI analysis: genuinely ambiguous points
    interactions: List[InteractionRecord] = Field(default_factory=list)
    student_interpretation: str = ""
    active_target_id: str = ""
    active_target_reason: str = ""                                    # why this demand is the current target (dev-mode)
    current_scaffold: Optional[dict] = None
    stage: str = "interpret"                 # interpret | mapping | restatement | adequate
    representation_adequate: bool = False
    restart_count: int = 0
    developer_notes: str = ""                                        # PRIVATE — never shown to students
    created_at: str = ""
    updated_at: str = ""


class CreateReq(BaseModel):
    assignment_text: str


class TextReq(BaseModel):
    text: str


# ---------------------------------------------------------------------------
# LLM plumbing
# ---------------------------------------------------------------------------
_TONE = (
    "TONE: You are Compass, an expert tutor — warm, calm, economical, purposeful. Every sentence moves "
    "learning forward. NEVER use praise or filler ('Great job!', 'Excellent!', 'Nice work!'). No long "
    "monologues. Keep language plain and short."
)

_BOUNDARY = (
    "BOUNDARY: Lead with the assignment's demands and the intellectual operations they require. Use the "
    "student's words diagnostically. Do NOT write the assignment response, a thesis, an outline, an essay, "
    "or a polished answer. Distinguish EXPLICIT requirements (stated in the assignment — quote the wording) "
    "from INFERRED requirements (implied by the task). Scaffold ONE high-leverage demand at a time. Require "
    "the student to PERFORM the target operation. Compass teaches developmental OPERATIONS, not just demands."
)


def _extract_json(text: str) -> dict:
    text = (text or "").strip()
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


async def _llm(system: str, user: str, sid: str) -> dict:
    chat = LlmChat(api_key=_llm_key, session_id=sid, system_message=system).with_model(
        "anthropic", "claude-sonnet-4-6"
    )
    raw = await chat.send_message(UserMessage(text=user))
    return _extract_json(raw)


# ---------------------------------------------------------------------------
# Backend functions
# ---------------------------------------------------------------------------
async def analyze_assignment(assignment_text: str, sid: str):
    system = (
        "You analyze an assignment to extract the DEMANDS it places on the student — the things the student "
        "must understand and DO to represent the task adequately. " + _BOUNDARY + " " + _TONE + "\n\n"
        "For EACH demand return: label (short), description (one sentence), source ('explicit'|'inferred'), "
        "supporting_wording (exact quote from the assignment if explicit, else \"\"), operation (the single "
        "developmental operation the student must perform: e.g. Differentiate, Compare, Define, Explain, "
        "Exemplify, Relate, Analyze, Evaluate), concepts (1-3 key concepts), importance ('essential'|'supporting'), "
        "derivable_from_assignment (true if a careful reading of the assignment gives enough to discover this; "
        "false if it needs outside concept knowledge). Extract 3-6 demands. ALSO return important_distinctions "
        "(the key conceptual distinctions the task hinges on, e.g. 'learning process vs. learning outcome') and "
        "ambiguities (genuinely unclear points a student could reasonably read more than one way). Return ONLY JSON: "
        '{"demands":[{"label":"","description":"","source":"","supporting_wording":"","operation":"",'
        '"concepts":[],"importance":"","derivable_from_assignment":true}],"important_distinctions":[],"ambiguities":[]}'
    )
    data = await _llm(system, f"ASSIGNMENT:\n{assignment_text}", sid)
    out = []
    for d in data.get("demands", []):
        out.append(AssignmentDemand(
            label=d.get("label", "").strip() or "Requirement",
            description=d.get("description", ""),
            source="inferred" if str(d.get("source", "")).lower().startswith("infer") else "explicit",
            supporting_wording=d.get("supporting_wording", "") or "",
            operation=d.get("operation", ""),
            concepts=d.get("concepts", []) or [],
            importance="supporting" if str(d.get("importance", "")).lower().startswith("support") else "essential",
            derivable_from_assignment=bool(d.get("derivable_from_assignment", True)),
        ))
    return out, data.get("important_distinctions", []) or [], data.get("ambiguities", []) or []


_STATUS = {"understood", "developing", "needs_attention", "unconfirmed"}


def _norm_status(s: str, default: str = "unconfirmed") -> str:
    s = str(s or "").lower().replace(" ", "_")
    return s if s in _STATUS else default


async def compare_interpretation(sess: AssignmentSession, interpretation: str) -> dict:
    demands_brief = [
        {"id": d.id, "label": d.label, "operation": d.operation, "source": d.source,
         "description": d.description} for d in sess.demands
    ]
    system = (
        "The student has explained, in their own words, what they think the assignment asks. Compare this "
        "explanation DIAGNOSTICALLY against each demand. Do NOT teach or correct here — only diagnose. " + _BOUNDARY + "\n\n"
        "For each demand id return status and learner_evidence (what in the student's words shows understanding "
        "or misunderstanding). status: 'understood' (clearly grasped), 'developing' (partial/implicit), "
        "'needs_attention' (addressed but misunderstood/confused), 'unconfirmed' (not addressed). Also confidence "
        "0.0-1.0 (internal). Return ONLY JSON: "
        '{"demands":[{"id":"","status":"","learner_evidence":"","confidence":0.0}]}'
    )
    user = (f"ASSIGNMENT:\n{sess.assignment_text}\n\nDEMANDS:\n{json.dumps(demands_brief)}\n\n"
            f"STUDENT EXPLANATION:\n{interpretation}")
    return await _llm(system, user, sess.id)


async def generate_scaffold(sess: AssignmentSession, demand: AssignmentDemand, level: int) -> Scaffold:
    ladder = (
        "SCAFFOLD LADDER (escalates the learner's OPPORTUNITY TO PERFORM, not just the amount of instruction):\n"
        "0 Independent performance — minimal prompt; simply ask the student to perform the operation.\n"
        "1 Attention-directing cue — focus the student's attention on the relevant distinction/wording; do NOT teach.\n"
        "2 Guided construction — provide just enough structure (a frame, a contrast, a partial scaffold) for the "
        "student to perform the operation themselves.\n"
        "3 Direct teaching — teach the concept explicitly and briefly, THEN require the student to reconstruct it "
        "in their OWN WORDS (this reconstruction is MANDATORY; set requires_reconstruction=true)."
    )
    system = (
        "Produce ONE developmental scaffold for the TARGET demand at the given LEVEL. " + _BOUNDARY + " " + _TONE + "\n\n"
        + ladder + "\n\n"
        "Every scaffold MUST name the developmental operation being taught and execute a developmental MOVE — not "
        "a free-form chat. Return ONLY JSON with EXACTLY these fields: "
        '{"instructionType":"independent|attention_cue|guided_construction|direct_teaching","targetOperation":"",'
        '"concepts":[],"relevant_wording":"the assignment wording this points at","studentTask":"what the student '
        'must DO now (must require performing the operation)","expectedEvidence":"what a successful performance '
        'shows","nextIfSuccessful":"","nextIfUnsuccessful":"","requires_reconstruction":false}. '
        "studentTask is the message shown to the student: it may briefly set up the concept (more at higher levels) "
        "but MUST end by asking the student to perform the operation. At level 3 you TEACH then require reconstruction. "
        "Keep it short."
    )
    user = (f"ASSIGNMENT:\n{sess.assignment_text}\n\nTARGET DEMAND:\n"
            f"{json.dumps({'label': demand.label, 'description': demand.description, 'operation': demand.operation, 'concepts': demand.concepts, 'source': demand.source, 'supporting_wording': demand.supporting_wording, 'status': demand.status, 'learner_evidence': demand.learner_evidence, 'derivable_from_assignment': demand.derivable_from_assignment})}\n\n"
            f"SCAFFOLD LEVEL: {level}\n"
            f"PRIOR ATTEMPTS ON THIS DEMAND: {demand.scaffold_attempts}")
    data = await _llm(system, user, sess.id)
    itype = data.get("instructionType", "") or ["independent", "attention_cue", "guided_construction", "direct_teaching"][min(level, 3)]
    return Scaffold(
        demand_id=demand.id,
        level=level,
        instructionType=itype,
        targetOperation=data.get("targetOperation", demand.operation),
        concepts=data.get("concepts", demand.concepts) or demand.concepts,
        relevant_wording=data.get("relevant_wording", demand.supporting_wording) or demand.supporting_wording,
        studentTask=data.get("studentTask", ""),
        expectedEvidence=data.get("expectedEvidence", ""),
        nextIfSuccessful=data.get("nextIfSuccessful", ""),
        nextIfUnsuccessful=data.get("nextIfUnsuccessful", ""),
        requires_reconstruction=bool(data.get("requires_reconstruction", level >= 3)),
    )


async def evaluate_operation(sess: AssignmentSession, demand: AssignmentDemand, scaffold: dict, student_text: str) -> dict:
    system = (
        "Determine whether the student PERFORMED the target developmental operation. Diagnose only; do NOT reveal "
        "the answer or write it for them. " + _BOUNDARY + "\n\n"
        "If the student wrote something like 'I don't know' or made no real attempt, performed=false and "
        "reason='no_attempt'. If they attempted but it is wrong/confused, reason='misconception'. If partial, "
        "reason='partial'. If they performed it, reason='success'. If the scaffold required a reconstruction (own "
        "words) and they did not reconstruct, performed=false reason='no_reconstruction'. Return ONLY JSON: "
        '{"performed":true,"status":"understood|developing|needs_attention","learner_evidence":"","reason":"","confidence":0.0}'
    )
    user = (f"ASSIGNMENT:\n{sess.assignment_text}\n\nTARGET DEMAND:\n"
            f"{json.dumps({'label': demand.label, 'operation': demand.operation, 'description': demand.description})}\n\n"
            f"SCAFFOLD:\n{json.dumps({'studentTask': scaffold.get('studentTask'), 'expectedEvidence': scaffold.get('expectedEvidence'), 'requires_reconstruction': scaffold.get('requires_reconstruction')})}\n\n"
            f"STUDENT RESPONSE:\n{student_text}")
    return await _llm(system, user, sess.id)


async def evaluate_restatement(sess: AssignmentSession, restatement: str) -> dict:
    demands_brief = [{"id": d.id, "label": d.label, "operation": d.operation,
                      "importance": d.importance, "source": d.source} for d in sess.demands]
    system = (
        "The student has restated the WHOLE assignment in their own words. Evaluate whether their representation "
        "is ADEQUATE FOR NOW — meaning every ESSENTIAL demand is at least developing and none is missing or "
        "misunderstood. Adequate-for-now does NOT mean perfect. " + _BOUNDARY + "\n\n"
        "Return per-demand status + learner_evidence, an overall 'adequate' boolean, and 'unresolved' (ids of "
        "essential demands still needing attention). Return ONLY JSON: "
        '{"adequate":true,"demands":[{"id":"","status":"","learner_evidence":""}],"unresolved":[]}'
    )
    user = (f"ASSIGNMENT:\n{sess.assignment_text}\n\nDEMANDS:\n{json.dumps(demands_brief)}\n\n"
            f"STUDENT RESTATEMENT:\n{restatement}")
    return await _llm(system, user, sess.id)


# ---------------------------------------------------------------------------
# Control logic (deterministic — no LLM)
# ---------------------------------------------------------------------------
UNRESOLVED = {"needs_attention", "unconfirmed"}


def _essential_unresolved(sess: AssignmentSession) -> List[AssignmentDemand]:
    return [d for d in sess.demands if d.importance == "essential" and d.status in UNRESOLVED]


def _pick_target(sess: AssignmentSession) -> Optional[AssignmentDemand]:
    """Highest-leverage unresolved essential demand: a misunderstanding (needs_attention)
    outranks an unaddressed one (unconfirmed); then original order is preserved."""
    unresolved = _essential_unresolved(sess)
    if not unresolved:
        # fall back to supporting demands only if no essential remains
        unresolved = [d for d in sess.demands if d.status in UNRESOLVED]
    if not unresolved:
        return None
    unresolved.sort(key=lambda d: (0 if d.status == "needs_attention" else 1,
                                    sess.demands.index(d)))
    return unresolved[0]


def _start_level(demand: AssignmentDemand) -> int:
    """First scaffold level for a freshly-selected target. A misunderstanding starts a
    touch higher than an unaddressed-but-derivable demand. Non-derivable demands start
    at guided construction so we don't leave the learner stranded."""
    if not demand.derivable_from_assignment:
        return 2
    return 2 if demand.status == "needs_attention" else 1


def determine_next_move(sess: AssignmentSession) -> dict:
    """Returns {'move': 'scaffold'|'restatement', 'target_id': str, 'level': int}."""
    if not _essential_unresolved(sess):
        return {"move": "restatement", "target_id": "", "level": 0}
    target = _pick_target(sess)
    if target is None:
        return {"move": "restatement", "target_id": "", "level": 0}
    return {"move": "scaffold", "target_id": target.id, "level": _start_level(target)}


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------
def _demand_by_id(sess: AssignmentSession, did: str) -> Optional[AssignmentDemand]:
    return next((d for d in sess.demands if d.id == did), None)


def _target_reason(d: AssignmentDemand) -> str:
    if d.status == "needs_attention":
        base = "Student addressed this but misunderstood it."
    elif d.status == "unconfirmed":
        base = "Student did not address this in their interpretation."
    elif d.status == "developing":
        base = "Student showed partial understanding; sharpening it."
    else:
        base = "Selected as the current developmental target."
    if d.learner_evidence:
        base += f" ({d.learner_evidence})"
    return base


async def _load(session_id: str) -> AssignmentSession:
    doc = await _db.assignment_sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Assignment session not found")
    return AssignmentSession(**doc)


async def _save(sess: AssignmentSession) -> AssignmentSession:
    sess.updated_at = _now_iso()
    await _db.assignment_sessions.update_one(
        {"id": sess.id}, {"$set": sess.model_dump()}, upsert=True
    )
    return sess


async def _advance_after_diagnosis(sess: AssignmentSession):
    """After statuses are updated, choose the next move and (if scaffolding) generate it."""
    move = determine_next_move(sess)
    if move["move"] == "restatement":
        sess.active_target_id = ""
        sess.current_scaffold = None
        sess.stage = "restatement"
        return
    target = _demand_by_id(sess, move["target_id"])
    target.scaffold_level = move["level"]
    scaffold = await generate_scaffold(sess, target, move["level"])
    sess.active_target_id = target.id
    sess.active_target_reason = _target_reason(target)
    sess.current_scaffold = scaffold.model_dump()
    sess.stage = "mapping"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post("/sessions", response_model=AssignmentSession)
async def create_session(req: CreateReq):
    text = (req.assignment_text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Assignment text is required.")
    sess = AssignmentSession(assignment_text=text, created_at=_now_iso(), updated_at=_now_iso())
    sess.demands, sess.important_distinctions, sess.ambiguities = await analyze_assignment(text, sess.id)
    sess.stage = "interpret"
    await _save(sess)
    return sess


@router.get("/sessions/{session_id}", response_model=AssignmentSession)
async def get_session(session_id: str):
    return await _load(session_id)


@router.patch("/sessions/{session_id}", response_model=AssignmentSession)
async def edit_assignment(session_id: str, req: CreateReq):
    """Edit the assignment and restart analysis (learner is warned client-side first)."""
    sess = await _load(session_id)
    text = (req.assignment_text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Assignment text is required.")
    sess.assignment_text = text
    sess.demands, sess.important_distinctions, sess.ambiguities = await analyze_assignment(text, sess.id)
    sess.interactions = []
    sess.student_interpretation = ""
    sess.active_target_id = ""
    sess.active_target_reason = ""
    sess.current_scaffold = None
    sess.representation_adequate = False
    sess.restart_count += 1
    sess.stage = "interpret"
    await _save(sess)
    return sess


@router.post("/sessions/{session_id}/interpret", response_model=AssignmentSession)
async def interpret(session_id: str, req: TextReq):
    sess = await _load(session_id)
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please explain the assignment first.")
    sess.student_interpretation = text
    diag = await compare_interpretation(sess, text)
    for d in diag.get("demands", []):
        dem = _demand_by_id(sess, d.get("id", ""))
        if dem:
            dem.status = _norm_status(d.get("status"), dem.status)
            dem.learner_evidence = d.get("learner_evidence", dem.learner_evidence)
            dem.confidence = float(d.get("confidence", dem.confidence) or 0.0)
    sess.interactions.append(InteractionRecord(
        kind="interpretation", student_text=text, evaluation=diag, created_at=_now_iso()))
    await _advance_after_diagnosis(sess)
    await _save(sess)
    return sess


@router.post("/sessions/{session_id}/operation", response_model=AssignmentSession)
async def operation(session_id: str, req: TextReq):
    sess = await _load(session_id)
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please write your response first.")
    target = _demand_by_id(sess, sess.active_target_id)
    if not target or not sess.current_scaffold:
        raise HTTPException(status_code=409, detail="No active developmental target.")
    ev = await evaluate_operation(sess, target, sess.current_scaffold, text)
    scaffold_snapshot = dict(sess.current_scaffold or {})
    target.scaffold_attempts += 1
    performed = bool(ev.get("performed"))
    if performed:
        target.status = _norm_status(ev.get("status"), "developing")
        if target.status in UNRESOLVED:
            target.status = "developing"
    else:
        # unsuccessful → escalate the opportunity to perform (cap at direct teaching)
        target.status = _norm_status(ev.get("status"), "needs_attention")
        if target.status not in UNRESOLVED:
            target.status = "needs_attention"
        target.scaffold_level = min(3, max(target.scaffold_level, sess.current_scaffold.get("level", 1)) + 1)
    target.learner_evidence = ev.get("learner_evidence", target.learner_evidence)
    target.confidence = float(ev.get("confidence", target.confidence) or 0.0)
    sess.interactions.append(InteractionRecord(
        kind="operation", student_text=text, target_demand_id=target.id,
        scaffold=scaffold_snapshot, evaluation=ev, created_at=_now_iso()))

    # Anti-trap: after repeated unsuccessful attempts at direct teaching, treat this
    # demand as 'developing' (adequate FOR NOW, not permanently complete) and move on,
    # rather than looping the same target forever.
    stuck = (not performed) and target.scaffold_level >= 3 and target.scaffold_attempts >= 3
    if stuck:
        target.status = "developing"

    if performed or stuck:
        await _advance_after_diagnosis(sess)
    else:
        # stay on the same target, but re-generate at the escalated level
        sess.active_target_reason = "Learner could not yet perform the operation; escalating support."
        scaffold = await generate_scaffold(sess, target, target.scaffold_level)
        sess.current_scaffold = scaffold.model_dump()
        sess.stage = "mapping"
    await _save(sess)
    return sess


@router.post("/sessions/{session_id}/restatement", response_model=AssignmentSession)
async def restatement(session_id: str, req: TextReq):
    sess = await _load(session_id)
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please restate the assignment first.")
    ev = await evaluate_restatement(sess, text)
    for d in ev.get("demands", []):
        dem = _demand_by_id(sess, d.get("id", ""))
        if dem:
            dem.status = _norm_status(d.get("status"), dem.status)
            dem.learner_evidence = d.get("learner_evidence", dem.learner_evidence)
    sess.interactions.append(InteractionRecord(
        kind="restatement", student_text=text, evaluation=ev, created_at=_now_iso()))

    if bool(ev.get("adequate")) and not _essential_unresolved(sess):
        sess.representation_adequate = True
        sess.active_target_id = ""
        sess.current_scaffold = None
        sess.stage = "adequate"
    else:
        # not adequate yet — return to scaffolding the highest-leverage remaining demand
        await _advance_after_diagnosis(sess)
    await _save(sess)
    return sess



# ---------------------------------------------------------------------------
# Developer instruments — Development Session record + private notes.
# (Not analytics. Each session is a complete, human-analyzable research case.)
# ---------------------------------------------------------------------------
class NotesReq(BaseModel):
    developer_notes: str = ""


def _duration_seconds(sess: AssignmentSession):
    try:
        from datetime import datetime
        a = datetime.fromisoformat(sess.created_at.replace("Z", "+00:00"))
        b = datetime.fromisoformat(sess.updated_at.replace("Z", "+00:00"))
        return max(0, int((b - a).total_seconds()))
    except Exception:
        return None


def build_record(sess: AssignmentSession) -> dict:
    explicit = [d for d in sess.demands if d.source == "explicit"]
    inferred = [d for d in sess.demands if d.source == "inferred"]

    def dbrief(d: AssignmentDemand):
        return {"label": d.label, "description": d.description, "operation": d.operation,
                "concepts": d.concepts, "importance": d.importance,
                "supporting_wording": d.supporting_wording, "status": d.status,
                "learner_evidence": d.learner_evidence}

    ops = [i for i in sess.interactions if i.kind == "operation"]
    dev_history = []
    for i in ops:
        dem = _demand_by_id(sess, i.target_demand_id)
        sc = i.scaffold or {}
        ev = i.evaluation or {}
        dev_history.append({
            "target_demand": dem.label if dem else i.target_demand_id,
            "target_operation": sc.get("targetOperation") or (dem.operation if dem else ""),
            "scaffold_level": sc.get("level"),
            "instruction_type": sc.get("instructionType"),
            "student_response": i.student_text,
            "performed": bool(ev.get("performed")),
            "reason": ev.get("reason", ""),
            "final_demand_status": dem.status if dem else "",
        })

    responses = [{"kind": i.kind, "text": i.student_text} for i in sess.interactions if i.student_text]
    final_restatement = next(
        (i.student_text for i in reversed(sess.interactions) if i.kind == "restatement"), "")

    idk = any(
        (i.evaluation or {}).get("reason") == "no_attempt"
        or "don't know" in (i.student_text or "").lower()
        or "dont know" in (i.student_text or "").lower()
        or "do not know" in (i.student_text or "").lower()
        for i in ops
    )
    num_level3 = sum(1 for i in ops if (i.scaffold or {}).get("level") == 3)

    return {
        "session_id": sess.id,
        "assignment": {"original": sess.assignment_text},
        "ai_analysis": {
            "explicit_demands": [dbrief(d) for d in explicit],
            "inferred_demands": [dbrief(d) for d in inferred],
            "important_distinctions": sess.important_distinctions,
            "ambiguities": sess.ambiguities,
        },
        "student": {
            "initial_interpretation": sess.student_interpretation,
            "responses": responses,
            "final_integrated_restatement": final_restatement,
        },
        "developmental_history": dev_history,
        "final_question_map": [
            {"label": d.label, "source": d.source, "operation": d.operation,
             "importance": d.importance, "status": d.status,
             "scaffold_level": d.scaffold_level, "scaffold_attempts": d.scaffold_attempts}
            for d in sess.demands
        ],
        "metadata": {
            "created_at": sess.created_at,
            "updated_at": sess.updated_at,
            "session_length_seconds": _duration_seconds(sess),
            "num_scaffold_attempts": len(ops),
            "num_scaffold_targets": len({i.target_demand_id for i in ops}),
            "num_level3_interventions": num_level3,
            "i_dont_know_occurred": idk,
            "restart_occurred": sess.restart_count > 0,
            "restart_count": sess.restart_count,
            "representation_adequate": sess.representation_adequate,
            "stage": sess.stage,
        },
        "developer_notes": sess.developer_notes,
    }


def _record_markdown(r: dict) -> str:
    L = ["# Development Session", "", f"_Session {r['session_id']}_", "",
         "## Assignment", r["assignment"]["original"], "", "## AI Analysis", "", "### Explicit demands"]
    for d in r["ai_analysis"]["explicit_demands"]:
        L.append(f"- **{d['label']}** ({d['operation']}) — {d['description']}  \n  wording: “{d['supporting_wording']}”  \n  final status: {d['status']}")
    L += ["", "### Inferred demands"]
    for d in r["ai_analysis"]["inferred_demands"]:
        L.append(f"- **{d['label']}** ({d['operation']}) — {d['description']}  \n  final status: {d['status']}")
    L += ["", "### Important distinctions"] + [f"- {x}" for x in r["ai_analysis"]["important_distinctions"]]
    L += ["", "### Ambiguities"] + [f"- {x}" for x in r["ai_analysis"]["ambiguities"]]
    L += ["", "## Student", "", "**Initial interpretation:** " + (r["student"]["initial_interpretation"] or "—"), "", "**Responses:**"]
    for resp in r["student"]["responses"]:
        L.append(f"- _{resp['kind']}_: {resp['text']}")
    L += ["", "**Final integrated restatement:** " + (r["student"]["final_integrated_restatement"] or "—"),
          "", "## Developmental history"]
    for h in r["developmental_history"]:
        L.append(f"- **{h['target_demand']}** · op={h['target_operation']} · level={h['scaffold_level']} "
                 f"· {'performed' if h['performed'] else 'not performed'} ({h['reason']}) → status {h['final_demand_status']}")
    L += ["", "## Final Question Map"]
    for d in r["final_question_map"]:
        L.append(f"- [{d['source']}/{d['importance']}] **{d['label']}** ({d['operation']}) — {d['status']} "
                 f"(level {d['scaffold_level']}, {d['scaffold_attempts']} attempts)")
    m = r["metadata"]
    L += ["", "## Metadata",
          f"- Created: {m['created_at']}",
          f"- Length: {m['session_length_seconds']}s",
          f"- Scaffold attempts: {m['num_scaffold_attempts']} across {m['num_scaffold_targets']} demands",
          f"- Level-3 interventions: {m['num_level3_interventions']}",
          f"- 'I don't know' occurred: {m['i_dont_know_occurred']}",
          f"- Restart occurred: {m['restart_occurred']} (x{m['restart_count']})",
          f"- Representation adequate: {m['representation_adequate']}",
          "", "## Developer Notes", r["developer_notes"] or "_(none)_"]
    return "\n".join(L)


@router.get("/sessions/{session_id}/record")
async def development_record(session_id: str, format: str = "json"):
    from fastapi import Response
    sess = await _load(session_id)
    r = build_record(sess)
    if format == "markdown":
        return Response(_record_markdown(r), media_type="text/markdown",
                        headers={"Content-Disposition": f'attachment; filename="dev_session_{session_id[:12]}.md"'})
    return Response(json.dumps(r, indent=2, default=str), media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="dev_session_{session_id[:12]}.json"'})


@router.patch("/sessions/{session_id}/developer-notes", response_model=AssignmentSession)
async def set_developer_notes(session_id: str, req: NotesReq):
    sess = await _load(session_id)
    sess.developer_notes = req.developer_notes or ""
    await _save(sess)
    return sess
