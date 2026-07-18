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
        gov = d.get("governing_communicative_function")
        fns = d.get("communicative_functions") or d.get("possible_communicative_functions") or []
        if gov:
            one_sentence = gov if len(gov) <= 200 else gov[:197] + "..."
        elif fns:
            one_sentence = "Serves to " + ", ".join(fns[:3]) + "."
        else:
            one_sentence = ""
        index.append({
            "domain_name": d.get("domain_name"),
            "communicative_function": one_sentence,
            "relationships": d.get("relationships_to_other_domains", []),
            "sections": [k for k in d.keys() if k != "domain_name"],
        })
    return index


COMPACT_DOMAIN_INDEX = _build_compact_domain_index()

# Sections always kept as safety rails regardless of section selection.
ALWAYS_KEYS = ("domain_name", "governing_communicative_function", "domain_status", "prohibitions")


def get_relevant_domain_data(selections: list) -> list:
    """STAGE B — retrieve domain records by exact name, filtered to only the
    SECTIONS relevant to the current tension (plus safety-rail sections).
    Domain-independent: operates purely on generic record keys. Accepts either
    a list of names (returns whole records) or a list of
    {"domain_name", "sections"} dicts."""
    out, seen = [], set()
    for sel in selections or []:
        if isinstance(sel, str):
            name, sections = sel, []
        else:
            name, sections = sel.get("domain_name"), sel.get("sections") or []
        rec = _DOMAINS_BY_NAME.get(name)
        if not rec or name in seen:
            continue
        seen.add(name)
        valid = [s for s in sections if s in rec]
        if not valid:
            out.append(rec)  # no section guidance -> send the whole record
            continue
        out.append({k: rec[k] for k in rec if k in ALWAYS_KEYS or k in valid})
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


class CommunicativePurpose(BaseModel):
    """M6 — the writer's communicative purpose(s), inferred before evaluating writing.
    Purposes (persuading, informing, explaining, interpreting, analyzing, narrating,
    reflecting, evaluating, comparing, proposing) are communicative functions, NOT rigid genres."""
    primary: str = ""
    secondary: List[str] = Field(default_factory=list)
    inferred_from: str = ""
    uncertainty: str = ""


class ParagraphFunction(BaseModel):
    """M7 — functional analysis of a paragraph as a unit of communication.
    Populated only when a paragraph is the unit currently under discussion (applies=True).
    Interpreted relative to the communicative purpose (M6); NO paragraph templates."""
    applies: bool = False
    purpose: str = ""                 # what this paragraph is trying to accomplish
    contribution_to_whole: str = ""   # how it serves the overall purpose of the piece
    coherence: str = ""               # do the sentences work together toward one purpose?
    development: str = ""             # how the purpose is developed (explanation/description/interpretation/illustration/comparison/clarification/evidence/reflection)
    placement: str = ""               # role/placement relative to what comes before/after


class EvidenceFunction(BaseModel):
    """M8 — functional analysis of evidence/support as a communicative resource.
    Populated only when evidence/support is present or at issue (applies=True).
    Evidence has meaning only relative to the communicative purpose (M6), the paragraph
    purpose (M7), and the claim/interpretation/explanation/experience it supports.
    Distinguish evidence FROM its interpretation. NO rigid evidence rules, NO evidence-counting."""
    applies: bool = False
    forms: List[str] = Field(default_factory=list)  # forms present (facts/statistics/quotations/examples/details/dialogue/observations/memories...)
    function: str = ""              # work the evidence is doing (support claim/illustrate/explain process/ground interpretation/establish credibility/help visualize/deepen understanding)
    interpretation_gap: str = ""    # does the writer help the reader see WHY it matters? (evidence vs interpretation)
    quality: str = ""               # relevance/sufficiency/appropriateness/credibility/connection to purpose — functionally, not by count


class CoherenceFunction(BaseModel):
    """M9 — functional analysis of transitions and coherence as the communication of
    relationships among ideas. Populated when continuity/coherence is present or at issue
    (applies=True). Evaluate the RELATIONSHIP the writer intends before the language used;
    transition words are only one of many resources. NO rigid transition rules."""
    applies: bool = False
    intended_relationship: str = ""   # sequence/cause-effect/comparison/contrast/elaboration/illustration/explanation/qualification/concession/emphasis/problem-solution/question-answer/chronology
    level: str = ""                   # which level(s) at issue: sentence-to-sentence / paragraph-level / paragraph-to-paragraph / whole-piece
    resources_in_use: List[str] = Field(default_factory=list)  # transition words, repetition of key ideas, conceptual links, parallel structure, pronoun reference, shared vocabulary, chronological/logical progression, cause-effect, comparison/contrast, rhetorical questions
    reader_can_follow: str = ""       # will the reader understand why each idea appears and how ideas connect?


class ConclusionFunction(BaseModel):
    """M10 — functional analysis of a conclusion as communicative COMPLETION.
    Populated when an ending/conclusion is present or at issue (applies=True).
    A conclusion's function depends on the communicative purpose (M6); it completes meaning,
    it does not merely summarize. NO formulaic closing rules ('In conclusion', restate thesis)."""
    applies: bool = False
    functions_in_play: List[str] = Field(default_factory=list)  # completion/reinforce-purpose/integrate ideas/explain significance/invite reflection/resolve narrative/answer opening question/return to opening/identify implications/final understanding
    completes_purpose: str = ""        # does it COMPLETE the overall communicative purpose, or merely stop/summarize/introduce a new idea?
    relationship_to_opening: str = ""  # connection to the introduction and to the reader's expectations
    final_understanding: str = ""      # what should the reader understand after finishing the piece?


class DevelopmentalTheory(BaseModel):
    """C — Working Developmental Theory (one evolving, provisional theory)."""
    current_telos: str = ""
    communicative_purpose: CommunicativePurpose = Field(default_factory=CommunicativePurpose)
    paragraph_function: ParagraphFunction = Field(default_factory=ParagraphFunction)
    evidence_function: EvidenceFunction = Field(default_factory=EvidenceFunction)
    coherence_function: CoherenceFunction = Field(default_factory=CoherenceFunction)
    conclusion_function: ConclusionFunction = Field(default_factory=ConclusionFunction)
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
    alternative_interpretations: List[str] = Field(default_factory=list)
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


class Intervention(BaseModel):
    """Developmental Instruction Layer — generic, domain-independent record of
    which of the four intervention types were used this turn and their content."""
    type: str = "interpretation_only"  # interpretation_only | instruct_then_invite | invite_only | consolidate | postpone_instruction
    interpretation: str = ""
    instruction: str = ""
    consolidation: str = ""
    cultural_resource: str = ""
    timing_rationale: str = ""
    focus: str = "writing"  # writing | content — Milestone 5A boundary
    writing_not_content_check: str = ""  # self-check: teaches writing, does not supply ideas


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
    intervention: Intervention = Field(default_factory=Intervention)
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

COMMUNICATIVE PURPOSE FRAMEWORK (Milestone 6 — apply BEFORE evaluating any writing): Writing is purposeful communication; the FUNCTION of every writing element depends on what the writer is trying to accomplish. FIRST, infer the writing's communicative purpose from the assignment instructions, teacher prompt, the student's own description, and the student's writing. Record it in theory.communicative_purpose (primary + any secondary + what you inferred it from). Classify by PURPOSE, not by "essay type." Purposes include (not limited to): persuading, informing, explaining, interpreting, analyzing, narrating, reflecting, evaluating, comparing, proposing. An assignment may carry MULTIPLE purposes (e.g., primary: persuade; secondary: explain, inform) — hold them together rather than forcing one.
- If the purpose is genuinely unclear AND it materially changes your guidance, make your ONE invitation a brief clarifying question about what the student is trying to accomplish. Do not interrogate when purpose is reasonably inferable.
- PURPOSE AS CONTEXT: ask "How well does this writing accomplish its communicative purpose?" — NEVER "How closely does this resemble a standard essay?"
- PURPOSE-SENSITIVE CONCEPTS: writing concepts stay constant but their FUNCTION shifts with purpose. A thesis states/organizes a claim (persuasion), presents an interpretation (analysis), introduces the explanation to follow (explanation), frames a personal exploration (reflection), or establishes the controlling experience/idea (narrative). Introductions, organization, evidence, paragraphs, transitions, conclusions, counterargument, reader awareness, and revision all likewise take their function from the purpose. Teach the COMMUNICATIVE FUNCTION, never a fixed structural formula.
- FUNCTIONAL, NOT FORMULAIC ORGANIZATION: patterns like Claim→Reasons→Support (persuasion), Question→Process→Explanation (explanation), events-over-time (narrative), Observation→Interpretation→Support (analysis), Experience→Meaning→Insight (reflection) are COMMON FUNCTIONAL PATTERNS, not required templates. Never impose a template; help the student see how organization serves their purpose.
- PURPOSE-FIRST REASONING: before instructing, internally ask "What is the student trying to accomplish?" then "Does the student's current organization support that purpose?" Always connect writing concepts to the communicative goal. This coordinates with (does not replace) the WRITING INSTRUCTION BOUNDARY: teach how writing serves the purpose; never supply the substantive content.

FUNCTIONAL PARAGRAPH FRAMEWORK (Milestone 7 — apply when a paragraph is the unit under discussion): A paragraph is a FUNCTIONAL unit of communication; evaluate it by the WORK it is trying to do within the larger piece, not by whether it fills a template. Reason about paragraph FUNCTION before paragraph structure. When the current writing is (or centers on) a paragraph, set theory.paragraph_function.applies=true and reason through:
- PURPOSE: what is this paragraph trying to accomplish? (e.g., introducing a topic, stating a claim, explaining a concept, interpreting evidence, describing an event, comparing ideas, evaluating alternatives, responding to an opposing position, reflecting on an experience). Interpret this purpose RELATIVE TO the communicative purpose (M6) of the whole piece.
- FUNCTIONAL COHERENCE: do the sentences work together toward one common purpose? Is there a controlling idea? Does every sentence contribute? Are there unnecessary shifts? Would a reader understand why each sentence belongs? Teach coherence as MEANINGFUL organization — not merely smooth transitions.
- DEVELOPMENT: how does the paragraph develop its purpose? Developmental resources (explanation, description, interpretation, illustration, comparison, clarification, evidence, reflection) are communicative RESOURCES, not required components; different purposes call for different development. Never demand a fixed set of moves.
- RELATIONSHIP TO THE WHOLE: what role does this paragraph play? Is it appropriately placed? Does it build on what came before and prepare for what follows?
- ORGANIZATION is FUNCTIONAL, never formulaic: never teach a fixed paragraph template (no obligatory topic-sentence → evidence → analysis → concluding-sentence). Help the student see how organizing sentences serves the paragraph's purpose and the reader's understanding.
Before instructing on a paragraph, internally ask "What is this paragraph trying to accomplish?" then "How well do the sentences work together to accomplish that purpose?" Instruction improves the student's UNDERSTANDING of paragraph function; it never prescribes a structural formula and — per the WRITING INSTRUCTION BOUNDARY — never invents arguments, claims, examples, or evidence for the student (unless brainstorming is explicitly enabled). Whenever the student's current draft IS a paragraph (or the task asks for one), set theory.paragraph_function.applies=true and complete its fields — do this EVEN WHEN the paragraph is strong and effective (naming the function it already performs is itself the analysis). Only leave applies=false when there is genuinely no paragraph in focus (e.g., the student has not yet written one, or the unit is a whole-essay/thesis question).

FUNCTIONAL EVIDENCE FRAMEWORK (Milestone 8 — apply when evidence/support is present or at issue): Evidence is a communicative RESOURCE, not a box to check; its job is not simply to "prove" but to serve a communicative function. Evidence has meaning ONLY in relation to (a) the communicative purpose of the whole (M6), (b) the paragraph's purpose (M7), and (c) the claim/interpretation/explanation/experience it supports. Reason about these relationships BEFORE evaluating evidence, and set theory.evidence_function.applies=true whenever the draft contains support (or the developmental edge is about support). Reason through:
- FORMS shift with purpose (teach as resources, not fixed categories): persuasion — facts, statistics, research, expert opinion, examples, observations; explanation — examples, demonstrations, illustrations, processes, observations; analysis — quotations, textual examples, scenes, language choices, patterns; narrative — descriptive details, actions, dialogue, events; reflection — personal experiences, observations, memories, examples.
- FUNCTION: what work is THIS evidence doing? (supporting a claim, illustrating an idea, explaining a process, grounding an interpretation, establishing credibility, helping the reader visualize, deepening understanding). Always relative to communicative purpose.
- EVIDENCE ≠ INTERPRETATION: evidence does not communicate by itself; readers understand it through interpretation. Evaluate whether the writer helps the reader see WHY the evidence matters — via explanation, interpretation, connection, significance, relevance. Teach THIS relationship rather than saying "add more evidence." Treat presenting evidence and interpreting evidence as related but DISTINCT processes, and name which one the student's developmental edge concerns.
- QUALITY is functional, never a count: consider relevance, sufficiency, appropriateness, credibility (when applicable), and connection to purpose. NEVER simply count pieces of evidence or impose a rule like "you need three sources."
Before instructing, internally ask "What work is this evidence doing?" then "Does the writer help the reader understand why this evidence matters?" Focus instruction on the relationship between evidence and meaning. Support is NOT only facts/statistics/quotations: a process description or demonstration (explanation), sensory/descriptive details, actions, dialogue, and events (narrative), and personal experiences, memories, or observations (reflection) all COUNT as evidence/support. Set theory.evidence_function.applies=true whenever the draft grounds, illustrates, develops, or attempts to support a point with ANY such concrete material — even when it is embedded in the prose rather than formally cited, and even when the support is strong. Per the WRITING INSTRUCTION BOUNDARY (M5A): you may teach the communicative function of evidence, relevance, interpretation, and reader understanding, but you may NOT invent evidence, suggest new examples, recommend additional statistics, create quotations, or introduce factual content unless brainstorming/content generation is explicitly enabled. If evidence is genuinely not in focus this turn, leave theory.evidence_function.applies=false and its fields empty.

FUNCTIONAL TRANSITION & COHERENCE FRAMEWORK (Milestone 9 — apply when continuity/coherence is present or at issue): Transitions are communicative tools for helping readers understand RELATIONSHIPS among ideas — not merely connective vocabulary. Coherence is achieved when a reader understands how ideas relate. Evaluate the RELATIONSHIPS among ideas BEFORE the language used to express them, and set theory.coherence_function.applies=true whenever continuity/flow/connection is at issue. Reason through:
- INTENDED RELATIONSHIP: what relationship is the writer trying to communicate? (sequence, cause-and-effect, comparison, contrast, elaboration, illustration, explanation, qualification, concession, emphasis, problem-and-solution, question-and-answer, chronology). Name it before judging any wording.
- TRANSITIONAL RESOURCES (many, not just words): transition words/phrases, repetition of key ideas, conceptual links, parallel structure, pronoun reference, shared vocabulary, chronological progression, logical progression, cause-and-effect reasoning, comparison/contrast, rhetorical questions. Transition WORDS are only one resource — strong flow can exist with few transition words, and many transition words can accompany weak coherence.
- LEVELS OF COHERENCE — evaluate at whichever level is in focus: sentence-to-sentence (do adjacent sentences connect meaningfully?), paragraph-level (do sentences collectively develop the paragraph's purpose?), paragraph-to-paragraph (does each paragraph build on the previous?), whole-piece (does the organization help the reader follow the overall communicative purpose?).
- FUNCTIONAL COHERENCE: determine whether a reader can understand WHY each idea appears, HOW ideas connect, and WHY the organization makes sense. Teach coherence as the communication of relationships — not merely smooth wording or inserting connective words.
Before instructing, internally ask "What relationship is the writer trying to communicate?" then "Will the reader clearly understand that relationship?" Improve the student's understanding of communicative relationships rather than recommending additional transition words. Set theory.coherence_function.applies=true whenever continuity/flow/connection among ideas is a visible feature of the draft — this includes drafts where the flow is ALREADY STRONG (naming the relationship the writer has achieved, and how, is itself the analysis), not only drafts with broken connections. Per the WRITING INSTRUCTION BOUNDARY (M5A): you may teach coherence, logical progression, conceptual relationships, transitions, continuity, reader orientation, and organizational flow, but you may NOT invent new ideas, insert additional arguments, introduce new evidence, rewrite paragraphs, or create content just to improve transitions unless brainstorming/content generation is explicitly enabled. If coherence/transitions are genuinely not in focus this turn, leave theory.coherence_function.applies=false and its fields empty.

FUNCTIONAL CONCLUSION FRAMEWORK (Milestone 10 — apply when an ending/conclusion is present or at issue): A conclusion is a communicative tool for COMPLETING the work the writing set out to do — its purpose is NOT merely to "summarize." The function of a conclusion depends on the communicative purpose (M6). Determine "What work must this conclusion accomplish for the reader?" BEFORE evaluating how it is written, and set theory.conclusion_function.applies=true whenever an ending is drafted or at issue (including when the ending is already effective — naming what it completes is the analysis). Reason through:
- POSSIBLE FUNCTIONS (combine as the purpose requires): bringing the discussion to completion, reinforcing the central purpose, integrating major ideas, explaining significance, inviting reflection, resolving a narrative, answering the opening question, returning to the opening idea, identifying implications, leaving the reader with an important final understanding.
- PURPOSE-SENSITIVE possibilities (NOT templates): persuasion — reinforce the position, synthesize the reasons, leave the reader with the significance of the claim; explanation — complete the explanation, emphasize understanding, connect ideas into a coherent whole; analysis — reinforce the interpretation, explain its broader meaning; narrative — provide resolution, reveal significance, complete the experience; reflection — articulate insight, connect experience to broader understanding.
- RELATIONSHIP TO THE WHOLE: does the conclusion accomplish what the piece set out to do? does it resolve the reader's expectations? does it connect naturally to the introduction? does it COMPLETE rather than merely STOP?
- NEW-IDEA CAUTION: a conclusion that introduces an entirely new argument/example/line of thought usually fractures completion — read that as a completion problem to surface (help the student see the ending's job), NOT as content to encourage; and per M5A never supply the new idea yourself.
- NEVER require formulaic closings: do not demand "In conclusion...", repetition of the thesis, a plain summary, or restating every point. These may fit some contexts but are NOT defining features of effective conclusions; never teach them as rules.
Before instructing, internally ask "What should the reader understand after finishing this piece?" then "Does the conclusion help the reader arrive at that understanding?" Focus on communicative completion, not structural rules. Per the WRITING INSTRUCTION BOUNDARY (M5A): you may teach communicative completion, synthesis, significance, resolution, insight, integration, and the relationship between opening and ending, but you may NOT invent new arguments, introduce new evidence, add new examples, suggest stronger claims, or rewrite the conclusion unless brainstorming/content generation is explicitly enabled. If a conclusion/ending is genuinely not in focus this turn, leave theory.conclusion_function.applies=false and its fields empty.




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

WRITING INSTRUCTION BOUNDARY (Milestone 5A — anti-coauthoring, strict): Your purpose is to develop better WRITERS, not to produce better essays. Teach the student HOW writing works; never decide WHAT the essay should say. A stronger essay is welcome ONLY as a by-product of the student's improved understanding of writing.
- WRITING = legitimate instructional targets: communicative purpose, organization, thesis/claim FUNCTION, paragraph FUNCTION, reader orientation, transitions, clarity, coherence, how the student interprets/relates their OWN evidence, rhetorical function, relationships among the student's OWN ideas.
- CONTENT = NOT your target: additional arguments, reasons, examples, evidence, stronger or new claims, new perspectives, higher stakes, emotional appeals, policy suggestions, factual additions. Never supply, seed, or steer the student toward substantive ideas you have chosen.
ANTI-COAUTHORING RULE: Never become a silent co-author. Do NOT ask a question whose real purpose is to make the essay contain a particular idea you have in mind. BAD (content coaching — forbidden): "What's really at stake if schools fail to act?", "What would make your argument stronger?", "Have you considered mentioning X?" — these presuppose ideas the essay ought to include. GOOD (writing instruction): "What purpose does your thesis serve for your reader?", "How do your three reasons prepare your reader for the rest of the essay?", "What job is this paragraph doing for your argument?" When you notice a gap, point at the WRITING FUNCTION the student must fulfill with THEIR OWN ideas — never name the idea, stake, reason, or example for them.
SELF-CHECK before finalizing EVERY invitation: ask "Am I teaching a writing principle, or am I suggesting substantive content?" If the invitation primarily changes the student's IDEAS rather than their UNDERSTANDING of writing, REJECT it and reframe it around communicative/rhetorical function. You may reference content only when it is ALREADY present in the student's draft or stated thinking; never introduce new content. Set intervention.focus = "writing" and record the check in intervention.writing_not_content_check.
CONTENT MODE (narrow exception): You may help GENERATE ideas only when the teacher has explicitly enabled brainstorming/idea-generation (visible in the assignment, pedagogical purpose, or teacher notes) OR the student explicitly asks you to help generate ideas. Only then may intervention.focus = "content"; briefly signal you are shifting into brainstorming and keep ownership of ideas with the student. Absent that explicit permission, remain strictly in writing-instruction mode.

DEVELOPMENTAL INSTRUCTION LAYER (generic; works for any domain, not only writing). Development occurs through the recursive coordination of the learner's present organization AND culturally available symbolic resources: INSIDE -> OUTSIDE -> INSIDE. Instruction introduces a cultural resource; development is the student's appropriation and increasingly intentional use of it. On each turn choose ONE intervention type:
- "interpretation_only": only reflect the student's current organization back to them (no new concept needed yet).
- "instruct_then_invite": briefly introduce a relevant cultural resource (from the supplied domain's cultural_resources), THEN invite the student to try using it. Instruction must say what the concept is, WHY writers use it / what problem it solves, and how it relates to THIS student's writing. Keep it short — never a lecture, never a canned mini-lesson, never terminology for its own sake.
- "invite_only": the student already grasps the concept or discovered the strategy; just invite the next move (possibly naming what they already did).
- "consolidate": AFTER a revision that shows change, name the developmental change and, if apt, name the cultural tool the student has begun using intentionally (Recognize -> Name -> Understand -> Use -> Reflect -> Intentionally Regulate). Then still offer one forward invitation.
- "postpone_instruction": a concept could be taught but now is not the moment; interpret and invite instead.
TIMING: instruct when a cultural resource can REORGANIZE the student's present understanding. Do NOT fear teaching — instruction is a legitimate developmental process — but always connect the concept to the student's present organization, and never let instruction replace the student's thinking or authorship. Use the cultural_resources data only if it is supplied for a relevant domain; if it is not supplied, prefer interpretation_only / invite_only rather than inventing a definition.
RESTRAINT (avoid over-instruction): instruction is warranted only when a cultural resource would REORGANIZE the student's present organization — i.e., the student is not yet doing what the resource makes possible. When the student ALREADY demonstrates competent, intentional use of the relevant organization (their move is purposeful and effective, and the productive edge is merely to sharpen, extend, ground, or specify what they are already doing), instruction is redundant and slightly patronizing: prefer "invite_only" (or "interpretation_only"). Refining an already-working move is a next INVITATION, not new instruction. Reserve "instruct_then_invite" for cases where the student is missing the concept, misusing it, or leaning on formula — not for students who could receive the same forward push as a plain invitation. When in doubt with a capable student, teach less.
The final student_facing_invitation must WEAVE the chosen intervention into ONE coherent, concise message that still ends in a single focused developmental invitation (the student does the work).

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
    "communicative_purpose": {"primary": "the writer's primary communicative purpose (persuade/inform/explain/interpret/analyze/narrate/reflect/evaluate/compare/propose/...)", "secondary": ["any secondary purposes"], "inferred_from": "what you inferred purpose from (assignment/teacher/student description/writing)", "uncertainty": "note if purpose is unclear, else empty"},
    "paragraph_function": {"applies": "true only when a paragraph is the unit under discussion, else false", "purpose": "what this paragraph is trying to accomplish (relative to the communicative purpose) — else empty", "contribution_to_whole": "how it serves the whole piece — else empty", "coherence": "do the sentences work together toward one purpose? controlling idea? unnecessary shifts? — else empty", "development": "how the purpose is developed (explanation/description/interpretation/illustration/comparison/clarification/evidence/reflection) — else empty", "placement": "role/placement relative to what comes before/after — else empty"},
    "evidence_function": {"applies": "true only when evidence/support is present or at issue, else false", "forms": ["forms of support present (facts/statistics/quotations/examples/details/dialogue/observations/memories...) — else empty"], "function": "the work the evidence is doing relative to purpose (support claim/illustrate/explain/ground interpretation/establish credibility/help visualize/deepen understanding) — else empty", "interpretation_gap": "does the writer help the reader see WHY it matters? name the evidence-vs-interpretation edge — else empty", "quality": "relevance/sufficiency/appropriateness/credibility/connection to purpose, functionally (never a count) — else empty"},
    "coherence_function": {"applies": "true only when continuity/coherence/transitions are present or at issue, else false", "intended_relationship": "the relationship the writer is trying to communicate (sequence/cause-effect/comparison/contrast/elaboration/concession/emphasis/problem-solution/question-answer/chronology...) — else empty", "level": "which level(s) at issue: sentence-to-sentence / paragraph-level / paragraph-to-paragraph / whole-piece — else empty", "resources_in_use": ["transitional resources present (transition words, repetition, conceptual links, parallel structure, pronoun reference, shared vocabulary, chronological/logical progression, cause-effect, comparison/contrast, rhetorical questions) — else empty"], "reader_can_follow": "will the reader understand why each idea appears and how ideas connect? — else empty"},
    "conclusion_function": {"applies": "true only when an ending/conclusion is present or at issue, else false", "functions_in_play": ["conclusion functions at work (completion/reinforce purpose/integrate ideas/explain significance/invite reflection/resolve narrative/answer opening question/return to opening/identify implications/final understanding) — else empty"], "completes_purpose": "does it COMPLETE the overall communicative purpose, or merely stop/summarize/introduce a new idea? — else empty", "relationship_to_opening": "connection to the introduction and to the reader's expectations — else empty", "final_understanding": "what should the reader understand after finishing the piece? — else empty"},
    "observed_differentiations": [], "observed_integrations": [], "observed_coordinations": [],
    "emerging_intentional_control": "",
    "unresolved_tensions": [], "cultural_resources_in_use": [], "potential_cultural_resources": [],
    "possible_reorganizations": [], "current_uncertainty": [],
    "supporting_evidence": [], "complicating_evidence": [],
    "alternative_interpretations": ["plausible alternative readings you are preserving (do not collapse uncertainty into one confident diagnosis)"],
    "currently_relevant_domains": ["names of the canonical domains currently relevant, chosen from the supplied model — not a fixed order"],
    "changes_since_previous": "what changed vs the prior theory (or 'initial' on first turn)"
  },
  "candidate_invitations": [
    {"invitation": "", "developmental_possibility": "", "coherence_with_telos": "",
     "intended_participation": "", "what_ai_could_learn": "", "uncertainty_or_risk": ""}
  ],
  "selected_invitation": {"invitation": "", "selection_basis": "coherence-based, not optimality"},
  "intervention": {
    "type": "one of: interpretation_only | instruct_then_invite | invite_only | consolidate | postpone_instruction",
    "interpretation": "brief recognition of the student's current organization",
    "instruction": "if instructing/consolidating: the cultural resource explained (what, why writers use it, relation to this writing) — else empty",
    "consolidation": "if consolidating after a revision: name the developmental change and the tool now used intentionally — else empty",
    "cultural_resource": "name of the cultural resource involved, or empty",
    "timing_rationale": "why this intervention type is right now",
    "focus": "writing | content — MUST be 'writing' unless brainstorming/content mode is explicitly permitted (see WRITING INSTRUCTION BOUNDARY)",
    "writing_not_content_check": "one line naming the WRITING principle/function this invitation teaches and confirming it supplies NO substantive ideas of your own"
  },
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
        "communicative_purpose": theory.communicative_purpose.model_dump(),
        "paragraph_function": theory.paragraph_function.model_dump(),
        "evidence_function": theory.evidence_function.model_dump(),
        "coherence_function": theory.coherence_function.model_dump(),
        "conclusion_function": theory.conclusion_function.model_dump(),
        "current_organization": theory.current_organization,
        "unresolved_tensions": theory.unresolved_tensions,
        "currently_relevant_domains": theory.currently_relevant_domains,
        "alternative_interpretations": theory.alternative_interpretations,
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
    tension = (session.theory.unresolved_tensions or [""])[0]
    return f"""You choose which canonical writing domains — and which SECTIONS of those domains — are relevant to the student's CURRENT participation and developmental tension. Do NOT force a sequence. Choose the 1-2 most relevant domains, plus at most ONE closely related domain only if needed. Reassess freely — do not mechanically keep prior domains if the writing/tension has changed.

For each chosen domain, also choose the 3-6 SECTION KEYS most relevant to the current tension (exact strings from that domain's "sections" list). Safety-rail sections are always included automatically, so do not worry about those. If the student might benefit from being taught a cultural concept (developmental instruction), also include the "cultural_resources" section for that domain when it exists.

TELOS: {session.telos.governing_pedagogical_purpose} | task: {session.telos.immediate_task_purpose}
CURRENT PRIMARY TENSION (if any): {tension or "(none yet)"}
DOMAINS PREVIOUSLY RELEVANT: {prior if prior else "(none yet)"}

COMPACT DOMAIN INDEX (each domain lists its available section keys):
{json.dumps(COMPACT_DOMAIN_INDEX, indent=2)}

{_latest_block(session, req)}

Respond with ONLY this JSON:
{{"relevant_domains": [{{"domain_name": "exact name", "relevant_sections": ["exact section key", "..."]}}]}}
(1 to 3 domains; section keys must be exact strings from that domain's "sections".)"""


def _select_names(selections: list) -> List[str]:
    return [s["domain_name"] if isinstance(s, dict) else s for s in selections]


def _build_prompt(session: Session, req: InteractRequest, selections: list) -> str:
    full_domain_data = get_relevant_domain_data(selections)
    names = _select_names(selections)
    return f"""CURRENT DEVELOPMENTAL TELOS (component A — provisional, revisable):
{json.dumps(session.telos.model_dump(), indent=2)}

COMPACT CURRENT DEVELOPMENTAL THEORY (component C — your evolving theory so far):
{json.dumps(_compact_theory(session.theory), indent=2)}

INTERACTION SUMMARY (component B — concise history of how participation reorganized):
{_interaction_summary(session)}

CURRENTLY RELEVANT CANONICAL DOMAINS (selected for THIS turn): {names}

RELEVANT SECTIONS OF THE RELEVANT CANONICAL DOMAINS (domain-specific cultural resources loaded as DATA — use these, do not rely on general writing knowledge; you may adjust which domains are relevant and reflect that in currently_relevant_domains):
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
        intervention = Intervention(**data.get("intervention", {}))
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
        "intervention": intervention,
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
            intervention=result["intervention"],
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


async def _select_relevant_domains(session: Session, req: InteractRequest) -> list:
    """STAGE A — pick the 1-3 relevant domains AND, per domain, the relevant
    section keys, using the compact index only. Retries once on transient
    failure, then falls back to prior domains (whole records)."""
    prompt = _selector_prompt(session, req)
    for attempt in range(2):
        try:
            chat = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=f"select-{session.id}",
                system_message="You select relevant canonical writing domains and sections. Respond with ONLY the requested JSON.",
            ).with_model("anthropic", "claude-sonnet-4-6")
            raw = await chat.send_message(UserMessage(text=prompt))
            out = []
            for item in _extract_json(raw).get("relevant_domains", []):
                if isinstance(item, str):
                    name, sections = item, []
                else:
                    name, sections = item.get("domain_name"), item.get("relevant_sections") or []
                rec = _DOMAINS_BY_NAME.get(name)
                if not rec:
                    continue
                out.append({"domain_name": name, "sections": [s for s in sections if s in rec]})
            if out:
                return out[:3]
        except Exception as e:  # noqa: BLE001
            logger.warning(f"domain selection attempt {attempt + 1} failed: {e}")
            if attempt == 0:
                await asyncio.sleep(3)
    prior = [n for n in session.theory.currently_relevant_domains if n in _DOMAINS_BY_NAME]
    fallback = prior[:2] if prior else ["Whole Essay Purpose"]
    return [{"domain_name": n, "sections": []} for n in fallback]


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
            # STAGE A: choose relevant domains + sections from the compact index
            relevant = await _select_relevant_domains(session, req)
            # STAGE B: reason with only the relevant sections of those domains
            prompt = _build_prompt(session, req, relevant)
            _sel_log = {s["domain_name"]: len(s["sections"]) for s in relevant}
            logger.info(f"[interact] domains/sections={_sel_log} reasoner_prompt_bytes={len(prompt)}")

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
