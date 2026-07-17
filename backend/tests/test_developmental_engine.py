"""Backend tests for the Developmental Guide Engine.

Milestone under test (iteration_3):
- The engine is now DOMAIN-INDEPENDENT and consults a Canonical Writing Model
  loaded as DATA (backend/canonical_writing_model.json, 13 domains).
- Session persists: telos (A), interactions (B, with candidate_invitations +
  selected_invitation + observed_reorganization), theory (C, one evolving
  provisional working developmental theory), theory_history (previous
  theories preserved), and turns.
- No stages/levels/scores anywhere.
- Teacher can revise the telos via PATCH /api/sessions/{id}/telos.

Run serially:  pytest /app/backend/tests/test_developmental_engine.py -v -n 0
"""
import json
import os
import re
import time
from pathlib import Path

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    # fall back to the frontend .env so the tests can be run from the backend
    _envp = Path("/app/frontend/.env")
    if _envp.exists():
        for _line in _envp.read_text().splitlines():
            if _line.strip().startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = _line.split("=", 1)[1].strip()
                break
assert BASE_URL, "REACT_APP_BACKEND_URL must be set (in env or frontend/.env)"
BASE_URL = BASE_URL.rstrip("/")
API = f"{BASE_URL}/api"
LLM_TIMEOUT = 120  # Claude calls can take 10-30s; the prompt is now large


def post_interact_with_retry(client, sid, payload, retries=4, sleep_between=10):
    """Retry the interact endpoint once on transient gateway errors (502/503/504).

    The prompt now embeds the full canonical writing model, so responses are
    larger and occasionally hit Cloudflare's edge timeout. A one-shot retry is
    the right layer here — we still assert on the eventual body.
    """
    last = None
    for attempt in range(retries + 1):
        r = client.post(
            f"{API}/sessions/{sid}/interact",
            json=payload, timeout=LLM_TIMEOUT,
        )
        last = r
        if r.status_code not in (502, 503, 504):
            return r
        time.sleep(sleep_between)
    return last

# Load the 13 canonical domain names once
CANONICAL_PATH = Path("/app/backend/canonical_writing_model.json")
with open(CANONICAL_PATH, "r") as f:
    CANONICAL = json.load(f)
CANONICAL_DOMAIN_NAMES = [d["domain_name"] for d in CANONICAL["domains"]]
assert len(CANONICAL_DOMAIN_NAMES) == 13, (
    f"Expected 13 canonical domains, got {len(CANONICAL_DOMAIN_NAMES)}"
)

# Stage / score language that must NOT leak into student-facing text
STAGE_SCORE_PATTERNS = [
    r"\bstage\s*\d\b",
    r"\blevel\s*\d\b",
    r"\bgrade\s*\d\b",
    r"\b\d+\s*/\s*10\b",
    r"\b\d+\s*out\s*of\s*10\b",
    r"\bscore[sd]?\b\s*\d",
    r"\brubric\b",
    r"\btrait\s*score\b",
    r"\bdevelopmental\s*stage\s*\d\b",
]


def _has_stage_or_score_language(text: str) -> bool:
    low = text.lower()
    for pat in STAGE_SCORE_PATTERNS:
        if re.search(pat, low):
            return True
    return False


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def created_session(client):
    payload = {
        "assignment": "TEST_ Write an argumentative essay on whether cities should ban cars from downtown cores.",
        "pedagogical_purpose": (
            "Students should learn to organize an argument so each paragraph "
            "advances a single claim toward the thesis."
        ),
        "current_writing_task": "Draft the opening two paragraphs establishing your position.",
        "teacher_notes": "TEST_ student tends to list ideas rather than connect them.",
    }
    r = client.post(f"{API}/sessions", json=payload, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data.get("id"), str) and data["id"]
    assert data["assignment"] == payload["assignment"]
    assert data["pedagogical_purpose"] == payload["pedagogical_purpose"]
    assert data["current_writing_task"] == payload["current_writing_task"]
    assert data["turns"] == []
    assert data["interactions"] == []
    assert data["theory_history"] == []

    # telos seeded from teacher inputs
    telos = data["telos"]
    assert telos["governing_pedagogical_purpose"] == payload["pedagogical_purpose"]
    assert telos["immediate_task_purpose"] == payload["current_writing_task"]
    assert telos["assignment_context"] == payload["assignment"]
    assert telos["teacher_intentions"] == payload["teacher_notes"]

    # theory has expected default keys, all empty
    theory = data["theory"]
    for k in [
        "current_telos", "current_organization",
        "observed_differentiations", "observed_integrations",
        "observed_coordinations", "emerging_intentional_control",
        "unresolved_tensions", "cultural_resources_in_use",
        "potential_cultural_resources", "possible_reorganizations",
        "current_uncertainty", "supporting_evidence",
        "complicating_evidence", "currently_relevant_domains",
        "changes_since_previous",
    ]:
        assert k in theory, f"theory missing key {k}"
    assert theory["currently_relevant_domains"] == []
    return data


# ---------------------------------------------------------------------------
# Session creation (A — telos seeded from teacher inputs)
# ---------------------------------------------------------------------------
class TestSessionCreation:
    def test_session_created_with_seeded_telos(self, created_session):
        assert created_session["turns"] == []
        assert isinstance(created_session["telos"], dict)
        assert created_session["telos"]["governing_pedagogical_purpose"].strip() != ""
        assert created_session["telos"]["assignment_context"].strip() != ""


# ---------------------------------------------------------------------------
# First writing turn: currently_relevant_domains populated from canonical model,
# 2-3 candidate invitations, one selected, observed_reorganization present,
# theory_history has one snapshot preserving the PREVIOUS (empty) theory.
# ---------------------------------------------------------------------------
class TestFirstInteract:
    def test_first_writing_populates_theory_and_history(self, client, created_session):
        payload = {
            "kind": "writing",
            "content": (
                "Cars are bad. They cause pollution. Also they cause traffic. "
                "Also they are noisy. I think downtown should ban them because "
                "of these reasons. Downtown is where people live and work so "
                "it is important to make it nice."
            ),
        }
        r = post_interact_with_retry(client, created_session["id"], payload)
        assert r.status_code == 200, r.text
        data = r.json()
        pytest.first_interact_response = data

        # 2 turns: student then AI
        assert len(data["turns"]) == 2
        assert data["turns"][0]["role"] == "student" and data["turns"][0]["kind"] == "writing"
        assert data["turns"][1]["role"] == "ai" and data["turns"][1]["kind"] == "invitation"
        invitation = data["turns"][1]["content"].strip()
        assert invitation, "AI invitation is empty"

        # AI must NOT rewrite the student text
        assert "Cars are bad. They cause pollution." not in invitation, (
            "AI appears to have rewritten the student's paragraph"
        )
        # AI must NOT emit a numbered list of errors
        assert not (invitation.startswith("1.") and "2." in invitation and "3." in invitation), (
            "AI produced a numbered list of errors instead of a single invitation"
        )
        # No stage / score language
        assert not _has_stage_or_score_language(invitation), (
            f"Invitation leaks stage/score language: {invitation!r}"
        )

        # theory populated
        theory = data["theory"]
        rel = theory["currently_relevant_domains"]
        assert isinstance(rel, list) and len(rel) >= 1, (
            f"currently_relevant_domains empty after first turn: {rel!r}"
        )
        # every entry must come from the 13 canonical domain names
        for name in rel:
            assert name in CANONICAL_DOMAIN_NAMES, (
                f"'{name}' is not one of the 13 canonical domains {CANONICAL_DOMAIN_NAMES}"
            )
        assert theory["current_organization"].strip() != ""

        # interactions[-1] has 2 or 3 candidates, a selected invitation, and observed_reorganization
        assert len(data["interactions"]) == 1
        ir = data["interactions"][-1]
        assert 2 <= len(ir["candidate_invitations"]) <= 3, (
            f"expected 2-3 candidate_invitations, got {len(ir['candidate_invitations'])}"
        )
        assert ir["selected_invitation"]["invitation"].strip() != ""
        assert ir["observed_reorganization"].strip() != ""

        # theory_history has 1 snapshot preserving the PREVIOUS (empty) theory
        assert len(data["theory_history"]) == 1
        snap0 = data["theory_history"][0]
        assert snap0["version"] == 1
        assert snap0["theory"]["currently_relevant_domains"] == [], (
            "theory_history[0] should preserve the empty initial theory, not the new one"
        )

        # No numeric developmental scores anywhere in theory text
        theory_blob = json.dumps(theory)
        assert not _has_stage_or_score_language(theory_blob), (
            "Stage/score language leaked into theory"
        )


# ---------------------------------------------------------------------------
# Second interact (revise) — theory_history grows to 2, changes_since_previous
# is not 'initial', theory is REVISED (not appended), still no stages/scores.
# ---------------------------------------------------------------------------
class TestSecondInteract:
    def test_second_interact_revises_theory_and_history(self, client, created_session):
        first = getattr(pytest, "first_interact_response", None)
        assert first is not None, "First interact must run before this test"
        first_invitation = first["turns"][1]["content"].strip()
        first_domains = set(first["theory"]["currently_relevant_domains"])

        revised_draft = (
            "Banning cars from downtown would make the core dramatically more "
            "livable, and every part of my argument hangs from that single "
            "claim. First, air quality: without tailpipe exhaust concentrated "
            "in a few blocks, the people who work and live downtown breathe "
            "cleaner air, which is the basic condition of a livable place.\n\n"
            "Second, foot traffic and small shops: when streets are for "
            "people, walkers linger, and local businesses that depend on "
            "casual browsing — bookstores, cafes, produce stands — actually "
            "survive. Each of these follows from the livability claim; I am "
            "no longer just listing complaints about cars."
        )
        r = post_interact_with_retry(
            client, created_session["id"],
            {"kind": "revise", "content": revised_draft},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        pytest.second_interact_response = data

        # 4 turns now
        assert len(data["turns"]) == 4
        assert data["turns"][2]["kind"] == "revise"
        assert data["turns"][3]["role"] == "ai"

        second_invitation = data["turns"][3]["content"].strip()
        assert second_invitation != first_invitation
        assert not _has_stage_or_score_language(second_invitation)

        # revise must be acknowledged, never denied
        low = second_invitation.lower()
        for phrase in [
            "haven't revised", "have not revised", "you didn't revise",
            "no revision", "still the same draft", "same as before",
            "identical to your previous",
        ]:
            assert phrase not in low, (
                f"Coach denied the revision with {phrase!r}: {second_invitation!r}"
            )

        # theory_history now has 2 snapshots
        assert len(data["theory_history"]) == 2
        assert data["theory_history"][0]["version"] == 1
        assert data["theory_history"][1]["version"] == 2
        # v2 preserves the FIRST theory (which had non-empty relevant domains)
        assert data["theory_history"][1]["theory"]["currently_relevant_domains"] == list(first_domains) or \
            set(data["theory_history"][1]["theory"]["currently_relevant_domains"]) == first_domains, (
                "theory_history[1] should preserve the first-turn theory"
            )

        # changes_since_previous is not 'initial' anymore
        changes = data["theory"]["changes_since_previous"].strip().lower()
        assert changes != "" and changes != "initial", (
            f"changes_since_previous should reflect revision, got {changes!r}"
        )

        # currently_relevant_domains still drawn from canonical model
        rel = data["theory"]["currently_relevant_domains"]
        assert len(rel) >= 1
        for name in rel:
            assert name in CANONICAL_DOMAIN_NAMES

        # interactions grew to 2, latest has 2-3 candidates + selected
        assert len(data["interactions"]) == 2
        latest = data["interactions"][-1]
        assert 2 <= len(latest["candidate_invitations"]) <= 3
        assert latest["selected_invitation"]["invitation"].strip() != ""

        # theory REVISED, not appended: it is a single dict not a list of appended notes
        assert isinstance(data["theory"], dict)

        # No stages/scores in the theory blob or interactions blob
        assert not _has_stage_or_score_language(json.dumps(data["theory"]))
        assert not _has_stage_or_score_language(json.dumps(data["interactions"]))


# ---------------------------------------------------------------------------
# Teacher can revise the telos (PATCH /api/sessions/{id}/telos)
# ---------------------------------------------------------------------------
class TestTelosEdit:
    def test_patch_telos_updates_session_and_appends_teacher_edit(self, client, created_session):
        sid = created_session["id"]
        new_purpose = (
            "Students should learn to make every paragraph coordinate with a "
            "single governing claim about livability."
        )
        new_task = "Revise the opening two paragraphs so each supports the livability claim."
        r = client.patch(
            f"{API}/sessions/{sid}/telos",
            json={
                "pedagogical_purpose": new_purpose,
                "current_writing_task": new_task,
                "note": "TEST_ narrowing purpose after seeing first revision.",
            },
            timeout=30,
        )
        assert r.status_code == 200, r.text
        data = r.json()

        assert data["pedagogical_purpose"] == new_purpose
        assert data["current_writing_task"] == new_task
        # telos mirrored
        assert data["telos"]["governing_pedagogical_purpose"] == new_purpose
        assert data["telos"]["immediate_task_purpose"] == new_task
        assert data["telos"]["telos_changed"].strip() != ""

        # teacher_edits record appended
        assert len(data["teacher_edits"]) >= 1
        latest_edit = data["teacher_edits"][-1]
        assert "changes" in latest_edit
        assert "pedagogical_purpose" in latest_edit["changes"]
        assert latest_edit["changes"]["pedagogical_purpose"]["to"] == new_purpose

        # GET returns revised values
        g = client.get(f"{API}/sessions/{sid}", timeout=15)
        assert g.status_code == 200
        gdata = g.json()
        assert gdata["pedagogical_purpose"] == new_purpose
        assert gdata["current_writing_task"] == new_task
        assert gdata["telos"]["governing_pedagogical_purpose"] == new_purpose


# ---------------------------------------------------------------------------
# Persistence: GET returns session with turns, theory, theory_history, interactions
# ---------------------------------------------------------------------------
class TestPersistence:
    def test_get_session_returns_full_state(self, client, created_session):
        r = client.get(f"{API}/sessions/{created_session['id']}", timeout=15)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["id"] == created_session["id"]
        assert len(data["turns"]) == 4
        assert len(data["interactions"]) == 2
        assert len(data["theory_history"]) == 2
        assert data["turns"][1]["role"] == "ai"
        assert data["turns"][3]["role"] == "ai"
        # theory still populated
        assert len(data["theory"]["currently_relevant_domains"]) >= 1


# ---------------------------------------------------------------------------
# Regression: empty -> 400, missing session -> 404
# ---------------------------------------------------------------------------
class TestValidation:
    def test_empty_content_returns_400(self, client, created_session):
        r = client.post(
            f"{API}/sessions/{created_session['id']}/interact",
            json={"kind": "writing", "content": "   "},
            timeout=15,
        )
        assert r.status_code == 400, r.text

    def test_missing_session_returns_404(self, client):
        missing = f"nope-{int(time.time())}"
        r = client.get(f"{API}/sessions/{missing}", timeout=15)
        assert r.status_code == 404

        r2 = client.post(
            f"{API}/sessions/{missing}/interact",
            json={"kind": "writing", "content": "hello"},
            timeout=15,
        )
        assert r2.status_code == 404

        r3 = client.patch(
            f"{API}/sessions/{missing}/telos",
            json={"pedagogical_purpose": "x"},
            timeout=15,
        )
        assert r3.status_code == 404
