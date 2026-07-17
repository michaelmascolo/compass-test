import os
import json
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Any

from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

from emergentintegrations.llm.chat import LlmChat, UserMessage

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
# Models
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DevelopmentalState(BaseModel):
    governing_purpose: str = ""
    current_pedagogical_purpose: str = ""
    current_task: str = ""
    current_student_writing: str = ""
    organization_relative_to_purpose: str = ""
    direct_evidence: List[str] = Field(default_factory=list)
    primary_developmental_tension: str = ""
    alternative_interpretations: List[str] = Field(default_factory=list)
    developmental_movement: str = ""
    candidate_scaffolds: List[str] = Field(default_factory=list)
    selected_scaffold: str = ""
    selection_basis: str = ""
    uncertainties: List[str] = Field(default_factory=list)


class Turn(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # "student" or "ai"
    kind: str = "message"  # student: writing/revise/answer/explain/continue ; ai: invitation
    content: str
    created_at: str = Field(default_factory=now_iso)


class SessionCreate(BaseModel):
    assignment: str
    pedagogical_purpose: str
    current_writing_task: str
    teacher_notes: Optional[str] = ""


class InteractRequest(BaseModel):
    content: str
    kind: str = "writing"  # writing | revise | answer | explain | continue


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assignment: str
    pedagogical_purpose: str
    current_writing_task: str
    teacher_notes: Optional[str] = ""
    turns: List[Turn] = Field(default_factory=list)
    dev_state: DevelopmentalState = Field(default_factory=DevelopmentalState)
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)


# ---------------------------------------------------------------------------
# Developmental engine
# ---------------------------------------------------------------------------
SYSTEM_MESSAGE = """You are a developmental writing coach embedded in a research prototype. Your ONLY job is to help a student develop as a writer through scaffolded conversation. You NEVER edit, grade, or write for the student.

CORE PRINCIPLES (non-negotiable):
- Everything is organized around the teacher's pedagogical purpose.
- You evaluate the ORGANIZATION of the writing relative to that purpose, not surface errors or grammar.
- You maintain a compact working developmental theory and UPDATE it after every interaction (do not just append).
- All of your interpretations are provisional.
- You identify exactly ONE primary developmental tension at a time.
- You generate exactly ONE focused developmental invitation per turn.
- The student must do the cognitive and writing work. You must NEVER rewrite the student's paragraph or essay, never produce example essays or model paragraphs for them to copy.

WHAT YOU DO in your student-facing message: ask, invite, compare, focus attention, request a revision, or request an explanation. Keep it to ONE focused move. Warm, concise, specific to their actual text. No numbered lists of weaknesses. No indiscriminate praise. No diagnosing the student's personality or ability.

RETURN-TO-PURPOSE LOGIC:
- If the student misunderstands the assignment, move up to the assignment.
- If frustration blocks participation, address the frustration just enough to restore productive work.
- If the task is too hard, temporarily simplify the task, then return to the larger writing purpose.

PROCESS each turn:
1. Recover the current developmental state (provided below).
2. Read the student's latest writing/response.
3. Reconstruct the student's organization relative to the current purpose.
4. Identify ONE primary developmental tension.
5. Internally consider 2-3 possible invitations.
6. Pick the one best favored by evidence; if none dominates, pick one coherent invitation (no invented tie-breaker).
7. Output ONE student-facing invitation.
8. Update the developmental theory.

OUTPUT FORMAT — respond with ONLY a valid JSON object, no markdown, no prose outside it:
{
  "student_facing_invitation": "one focused, warm developmental move addressed to the student",
  "internal_state": {
    "governing_purpose": "the enduring writing-development purpose behind this assignment",
    "current_pedagogical_purpose": "the teacher's purpose, restated in working terms",
    "current_task": "what the student is being asked to do right now",
    "current_student_writing": "a short characterization of the latest writing (not a copy)",
    "organization_relative_to_purpose": "how the writing is organized relative to the purpose",
    "direct_evidence": ["short quotes or concrete observations from the student's text"],
    "primary_developmental_tension": "the single most important developmental tension right now",
    "alternative_interpretations": ["other plausible readings of what is going on"],
    "developmental_movement": "what changed since the previous state (or 'initial' on first turn)",
    "candidate_scaffolds": ["the 2-3 invitations you considered"],
    "selected_scaffold": "the invitation you chose",
    "selection_basis": "why this scaffold over the others, grounded in evidence",
    "uncertainties": ["what you are still unsure about"]
  }
}
"""


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


def _build_prompt(session: Session, req: InteractRequest) -> str:
    prior_state = session.dev_state.model_dump()
    history_lines = []
    for t in session.turns:
        who = "STUDENT" if t.role == "student" else "COACH"
        history_lines.append(f"{who} ({t.kind}): {t.content}")
    history = "\n\n".join(history_lines) if history_lines else "(no prior turns)"

    return f"""TEACHER SETUP
Assignment: {session.assignment}
Pedagogical Purpose: {session.pedagogical_purpose}
Current Writing Task: {session.current_writing_task}
Teacher Notes: {session.teacher_notes or "(none)"}

CURRENT DEVELOPMENTAL STATE (your working theory so far):
{json.dumps(prior_state, indent=2)}

CONVERSATION SO FAR:
{history}

STUDENT'S LATEST INPUT (kind = "{req.kind}"):
{req.content}

Now run the process and respond with ONLY the JSON object described in your instructions. Update (do not merely append to) the developmental state based on this latest input."""


async def run_engine(session: Session, req: InteractRequest) -> tuple[str, DevelopmentalState]:
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"dev-{session.id}",
        system_message=SYSTEM_MESSAGE,
    ).with_model("anthropic", "claude-sonnet-4-6")

    prompt = _build_prompt(session, req)
    raw = await chat.send_message(UserMessage(text=prompt))
    try:
        data = _extract_json(raw)
        invitation = data.get("student_facing_invitation", "").strip()
        state = DevelopmentalState(**{**session.dev_state.model_dump(), **data.get("internal_state", {})})
    except Exception as e:  # noqa: BLE001
        logger.error(f"Engine parse error: {e}; raw={raw[:500]}")
        raise HTTPException(status_code=502, detail="The developmental engine returned an unreadable response. Please try again.")
    if not invitation:
        raise HTTPException(status_code=502, detail="The developmental engine did not return an invitation. Please try again.")
    return invitation, state


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"message": "Developmental Writing Engine"}


@api_router.post("/sessions", response_model=Session)
async def create_session(payload: SessionCreate):
    session = Session(**payload.model_dump())
    await db.sessions.insert_one(session.model_dump())
    return session


@api_router.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    doc = await db.sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    return Session(**doc)


@api_router.post("/sessions/{session_id}/interact", response_model=Session)
async def interact(session_id: str, req: InteractRequest):
    doc = await db.sessions.find_one({"id": session_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    session = Session(**doc)

    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Empty submission")

    student_turn = Turn(role="student", kind=req.kind, content=req.content.strip())
    session.turns.append(student_turn)

    invitation, new_state = await run_engine(session, req)

    ai_turn = Turn(role="ai", kind="invitation", content=invitation)
    session.turns.append(ai_turn)
    session.dev_state = new_state
    session.updated_at = now_iso()

    await db.sessions.update_one(
        {"id": session_id},
        {"$set": {
            "turns": [t.model_dump() for t in session.turns],
            "dev_state": session.dev_state.model_dump(),
            "updated_at": session.updated_at,
        }},
    )
    return session


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
