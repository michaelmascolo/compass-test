"""
EXPERIMENTAL — Conditional Triage Architecture (latency workstream).

This module is an ADDITIVE, experimental reasoning path that runs ALONGSIDE the
frozen production engine (server._run_engine). It NEVER modifies the frozen
SYSTEM_MESSAGE or the constitutional commitments. STAGE 2 still uses the frozen
SYSTEM_MESSAGE verbatim; triage only (a) narrows what STAGE 2 must analyze and
(b) trims the serialized output — exactly the levers approved for the preview R3
trim, now generalized behind an explicit rapid-triage decision.

Pipeline:
  STAGE 1  RAPID TRIAGE (new, tiny system message, tiny output)
           -> what changed, prior-target status, learner state, instructional
              route, inside/outside, foundational?, highest-leverage dimension,
              relevant instructional objects, confidence.  (replaces STAGE-A)
  early-exit routing (code): stall -> stall support; unchanged prior target ->
           keep target; resolved -> assess fade/advance; foundational -> FULL
           exhaustive fallback (broad reassessment via server._run_engine).
  STAGE 2  FOCUSED ANALYSIS (frozen SYSTEM_MESSAGE + focused user prompt +
           trimmed output) -> the single coaching move for the triaged dimension.
"""
import json
import time
import asyncio

import server
from server import (
    SYSTEM_MESSAGE, EMERGENT_LLM_KEY, LlmChat, UserMessage,
    Session, Telos, InteractRequest, Turn, DevelopmentalObservation,
    _extract_json, _parse_engine_output, _compact_theory,
    get_relevant_domain_data, get_relevant_instructional_objects,
    build_instructional_network, _developmental_profile_summary,
    _latest_block, _previous_draft, SHARED_DEV_RESOURCES, _DOMAINS_BY_NAME,
)

MODEL = ("anthropic", "claude-sonnet-4-6")


def _tok(s: str) -> int:
    """Approximate token count (chars/4) — LlmChat does not surface usage."""
    return round(len(s or "") / 4)


# ---------------------------------------------------------------------------
# STAGE 1 — RAPID INSTRUCTIONAL TRIAGE
# ---------------------------------------------------------------------------
TRIAGE_SYSTEM_MESSAGE = """You are the RAPID INSTRUCTIONAL TRIAGE stage of a developmental writing coach (Compass). You do NOT coach the student and you do NOT write any student-facing text. Your only job is to decide, quickly and with minimal analysis, what the single highest-leverage next coaching move is and which narrow analysis the deep stage should perform. Eliminate irrelevant branches.

You are given a compact, incrementally-maintained learner state (not the full transcript) and the student's latest submission. Answer ONLY the triage questions. Prefer a plausible focused hypothesis over exhaustive certainty; the coach will observe the learner's next action and revise.

DECISIONS:
1. text_changed: what changed since the previous draft (or "first draft").
2. prev_target_status: resolved | partially_resolved | unchanged | worse | none.
3. learner_state: engaged | stalled | confused | finished_with_target.
4. instructional_route: exactly one of — stall_support | inside_out_clarification | outside_in_reader_task | convention_instruction | transfer_test | support_fading.
5. inside_or_outside: inside_out (learner does not yet have sufficient control of intended meaning / purpose / position / idea) | outside_in (minimally adequate intention is present, so test how the writing functions for a reader / task / convention). ROUTING INVARIANT: do NOT stay inside_out once intended meaning is sufficiently clear — move promptly to an outside_in test.
6. foundational_problem: true ONLY when a BROAD reassessment across many dimensions is genuinely required — this should be RARE (expect well under a quarter of turns). Set true only if ANY: (a) the draft does not actually address the assignment / is off-task; (b) the writer's basic intended meaning or overall communicative purpose cannot be determined at all; (c) the writing is so incoherent across ideas that no single dimension can be worked in isolation. Do NOT set foundational just because the draft is weak, missing a thesis, imperfect, or not yet succeeding at the assignment's named skill — those are handled by selecting the RIGHT single dimension in (7), NOT by broad reassessment. When one dimension is clearly highest-leverage, foundational_problem is false even if the draft is quite weak.
7. highest_leverage_dimension: the ONE dimension to work. ANTI-NARROWING RULE — do NOT default to "central claim"/"thesis"/"purpose alignment" out of habit. Choose central claim ONLY when the writer genuinely lacks a claim/position or the claim is absent/unarguable. If the draft ALREADY presents a workable claim/position, select the LIVE DOWNSTREAM EDGE instead (e.g., evidence-interpretation, causal reasoning, paragraph focus, transitions/coherence, point-of-view consistency, conclusion completion, sentence clarity, convention). If a PRIOR coaching target on a downstream element is unresolved, keep working THAT element — do not retreat upstream to the claim. Always honor the ASSIGNMENT PURPOSE: if it names a specific element, that element (not a generic thesis) is the default focus.
8. relevant_instructional_objects: 1-2 canonical element names most relevant to the dimension (e.g., "Thesis", "Central Claim", "Evidence", "Paragraph", "Introduction", "Purpose", "Reader", "Organization", "Transitions", "Conclusion").
9. route_confidence: 0.0-1.0.
10. rationale: one sentence.

Respond with ONLY this compact JSON (no prose, no code fence):
{"text_changed":"...","prev_target_status":"...","learner_state":"...","instructional_route":"...","inside_or_outside":"...","foundational_problem":false,"highest_leverage_dimension":"...","relevant_instructional_objects":["..."],"route_confidence":0.0,"rationale":"..."}"""


def _prev_target(session: Session) -> str:
    sc = session.theory.scaffolding_control
    return sc.primary_target or ""


def _triage_state_summary(session: Session, req: InteractRequest) -> str:
    """Compact, incrementally-derived learner state — NOT the full transcript."""
    th = session.theory
    prof = session.developmental_profile
    prev = _previous_draft(session)
    strengths = [f"{o.element}: {o.control_statement} ({o.trend})" for o in prof if o.trend in ("consolidating", "independent")]
    needs = [f"{o.element}: {o.control_statement} ({o.trend})" for o in prof if o.trend in ("confused", "emerging", "developing")]
    cp = th.communicative_purpose
    lines = [
        f"ASSIGNMENT PURPOSE (telos): {session.telos.governing_pedagogical_purpose or session.pedagogical_purpose}",
        f"IMMEDIATE TASK: {session.telos.immediate_task_purpose or session.current_writing_task}",
        f"INFERRED COMMUNICATIVE PURPOSE: primary={getattr(cp,'primary','') or '?'} secondary={getattr(cp,'secondary',[]) or []}",
        f"ACTIVE COACHING TARGET (prior turn): {_prev_target(session) or '(none yet)'}",
        f"PRIOR INSTRUCTIONAL MODE: {th.scaffolding_control.instructional_mode or '(none)'}",
        f"KNOWN STRENGTHS: {strengths or '(none recorded)'}",
        f"UNRESOLVED DEVELOPMENTAL NEEDS: {needs or '(none recorded)'}",
        f"SUBMISSION KIND: {req.kind}",
    ]
    if req.kind in server.DRAFT_KINDS:
        lines.append(f"PREVIOUS DRAFT:\n{prev if prev else '(none — first draft)'}")
        lines.append(f"CURRENT DRAFT:\n{req.content}")
    else:
        lines.append(f"STUDENT REPLY (not a new draft): {req.content}")
    return "\n".join(lines)


async def run_triage(session: Session, req: InteractRequest) -> dict:
    prompt = _triage_state_summary(session, req)
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"triage-{session.id}",
                   system_message=TRIAGE_SYSTEM_MESSAGE).with_model(*MODEL)
    t0 = time.perf_counter()
    raw = await chat.send_message(UserMessage(text=prompt))
    dt = time.perf_counter() - t0
    data = _extract_json(raw)
    data["_prompt_tokens"] = _tok(prompt)
    data["_output_tokens"] = _tok(raw)
    data["_latency_s"] = round(dt, 2)
    return data


# ---------------------------------------------------------------------------
# STAGE 2 — FOCUSED ANALYSIS (frozen SYSTEM_MESSAGE + focused user prompt)
# ---------------------------------------------------------------------------
FOCUSED_OUTPUT_OVERRIDE = """

=== FOCUSED ANALYSIS DIRECTIVE (rapid triage already ran) ===
A fast triage stage has ALREADY identified the single highest-leverage coaching target for THIS turn. Honor every rule, boundary, and constitutional commitment in your system message EXACTLY — anti-coauthoring, one student-facing invitation, never rewrite/supply content, respect competent performance. What changes is ONLY scope + payload, to reduce latency:
- Do NOT re-scan or re-diagnose every framework/rubric dimension. Analyze ONLY the triaged dimension below and the minimum context needed to interpret it.
- If prev_target_status is "unchanged", KEEP the same prior coaching target; do not search for a new one.
- If prev_target_status is "resolved", assess fade/advance (consolidate the gain; only advance if a clearly more important target has become primary).
- If learner_state is "stalled", give stall support on the current target — do not open a new target.
- Honor the inside/outside routing: if intended meaning is already sufficiently clear, do NOT linger in inside-out inquiry — test how the writing functions for a reader/task/convention.

TRIAGE DECISION:
{triage}

Serialize ONLY these top-level keys (omit all others — they are not needed this turn and omitting them changes nothing about your judgment):
{
  "student_facing_invitation": "...",
  "theory": {
    "communicative_purpose": {...},
    "scaffolding_control": {...},
    "instructional_reasoning": {...},
    "revision_development": {...}
  },
  "candidate_invitations": [...],
  "selected_invitation": {...},
  "intervention": {...}
}
theory.scaffolding_control MUST contain exactly one primary_target (the triaged dimension). Include theory.revision_development only when a prior draft exists to compare. Output compact JSON."""


def _focused_prompt(session: Session, req: InteractRequest, triage: dict, selections: list, io_names: list) -> str:
    full_domain_data = get_relevant_domain_data(selections)
    io_objects = get_relevant_instructional_objects(io_names or [])
    io_network = build_instructional_network(io_objects)
    override = FOCUSED_OUTPUT_OVERRIDE.replace("{triage}", json.dumps({
        k: triage.get(k) for k in (
            "instructional_route", "inside_or_outside", "prev_target_status",
            "learner_state", "highest_leverage_dimension", "route_confidence", "rationale")
    }, indent=2))
    return f"""CURRENT DEVELOPMENTAL TELOS (component A — provisional, revisable):
{json.dumps(session.telos.model_dump(), indent=2)}

COMPACT CURRENT DEVELOPMENTAL THEORY (component C — your evolving theory so far):
{json.dumps(_compact_theory(session.theory), indent=2)}

TRIAGED DIMENSION FOR THIS TURN (analyze ONLY this): {triage.get('highest_leverage_dimension')}
ROUTE: {triage.get('instructional_route')} | {triage.get('inside_or_outside')} | prior target status: {triage.get('prev_target_status')} | learner: {triage.get('learner_state')}

RELEVANT CANONICAL DOMAIN DATA (cultural resources loaded as DATA for the triaged dimension):
{json.dumps(full_domain_data, indent=2)}

RETRIEVED INSTRUCTIONAL OBJECTS (canonical knowledge that GOVERNS instruction — reason FROM these):
{json.dumps(io_objects, indent=2)}

INSTRUCTIONAL NETWORK (related elements — use for coherence only; still ONE target):
{json.dumps(io_network, indent=2)}

DEVELOPMENTAL PROFILE (accumulated control across prior episodes — scaffold from here):
{_developmental_profile_summary(session)}

SHARED DEVELOPMENTAL RESOURCE MENU:
{json.dumps(SHARED_DEV_RESOURCES, indent=2)}

{_latest_block(session, req)}

Run the governed instructional reasoning FOR THE TRIAGED DIMENSION ONLY, then respond with ONLY the JSON object described in your instructions.{override}"""


def _resolve_io(triage: dict):
    """Map triage's element names to (selections, io_names) without a STAGE-A call.
    Falls back to a whole-essay-purpose default when nothing matches."""
    io_names = [n for n in (triage.get("relevant_instructional_objects") or []) if isinstance(n, str)][:2]
    # map to canonical domains by loose containment
    dims = " ".join([triage.get("highest_leverage_dimension", "")] + io_names).lower()
    sel = []
    KEY = [
        ("Central Claim / Thesis", ("thesis", "claim", "position")),
        ("Opening / Introduction", ("intro", "opening", "hook")),
        ("Paragraph Purpose", ("paragraph", "topic sentence")),
        ("Whole Essay Purpose", ("purpose", "assignment", "whole")),
        ("Audience Awareness", ("reader", "audience")),
    ]
    for dom, kws in KEY:
        if dom in _DOMAINS_BY_NAME and any(k in dims for k in kws):
            sel.append({"domain_name": dom, "sections": []})
    if not sel:
        sel = [{"domain_name": "Whole Essay Purpose", "sections": []}] if "Whole Essay Purpose" in _DOMAINS_BY_NAME else []
    if not io_names:
        io_names = ["Thesis"]
    return sel[:3], io_names


async def run_focused(session: Session, req: InteractRequest, triage: dict) -> dict:
    selections, io_names = _resolve_io(triage)
    prompt = _focused_prompt(session, req, triage, selections, io_names)
    t0 = time.perf_counter()
    last_err = None
    raw = ""
    # Single retry on recoverable (unreadable / no-invitation) failures — parity
    # with the exhaustive path's retry. No other architectural change.
    for attempt in range(2):
        chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"focused-{session.id}-{attempt}",
                       system_message=SYSTEM_MESSAGE).with_model(*MODEL)
        raw = await chat.send_message(UserMessage(text=prompt))
        try:
            parsed = _parse_engine_output(session, raw)
            break
        except ValueError as e:
            last_err = e
            continue
    else:
        raise last_err
    dt = time.perf_counter() - t0
    parsed["_meta"] = {
        "focused_prompt_tokens": _tok(prompt),
        "focused_output_tokens": _tok(raw),
        "t_focused_s": round(dt, 2),
        "reasoner_prompt_bytes": len(prompt),
        "reasoner_output_bytes": len(raw),
    }
    return parsed


async def run_triage_pipeline(session: Session, req: InteractRequest) -> dict:
    """STAGE 1 triage -> early-exit routing -> STAGE 2 focused (or full fallback)."""
    t0 = time.perf_counter()
    triage = await run_triage(session, req)
    foundational = bool(triage.get("foundational_problem"))
    if foundational:
        # broad reassessment genuinely required -> use the full frozen engine
        result = await server._run_engine(session, req)
        m = result.get("_meta", {})
        result["_triage"] = triage
        result["_triage_meta"] = {
            "path": "foundational_fallback_full",
            "triage_latency_s": triage["_latency_s"],
            "triage_prompt_tokens": triage["_prompt_tokens"],
            "triage_output_tokens": triage["_output_tokens"],
            "focused_latency_s": None,
            "total_latency_s": round(time.perf_counter() - t0, 2),
            "num_model_calls": 1 + 1,  # triage + full stage-B (full also runs its own stage-A)
            "prompt_tokens": triage["_prompt_tokens"] + _tok("") + int((m.get("reasoner_prompt_bytes") or 0) / 4),
            "output_tokens": triage["_output_tokens"] + int((m.get("reasoner_output_bytes") or 0) / 4),
        }
        return result
    result = await run_focused(session, req, triage)
    fm = result["_meta"]
    result["_triage"] = triage
    result["_triage_meta"] = {
        "path": "triage_focused",
        "triage_latency_s": triage["_latency_s"],
        "focused_latency_s": fm["t_focused_s"],
        "total_latency_s": round(time.perf_counter() - t0, 2),
        "num_model_calls": 2,
        "prompt_tokens": triage["_prompt_tokens"] + fm["focused_prompt_tokens"],
        "output_tokens": triage["_output_tokens"] + fm["focused_output_tokens"],
    }
    return result


async def run_exhaustive(session: Session, req: InteractRequest) -> dict:
    t0 = time.perf_counter()
    result = await server._run_engine(session, req)
    m = result.get("_meta", {})
    result["_exhaustive_meta"] = {
        "path": "exhaustive_full",
        "stage_a_latency_s": m.get("t_stage_a_selector_s"),
        "stage_b_latency_s": m.get("t_stage_b_reasoner_s"),
        "total_latency_s": round(time.perf_counter() - t0, 2),
        "num_model_calls": 2,
        "prompt_tokens": int((m.get("reasoner_prompt_bytes") or 0) / 4),
        "output_tokens": int((m.get("reasoner_output_bytes") or 0) / 4),
    }
    return result
