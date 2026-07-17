"""Backend tests for the Developmental Writing Studio engine.

Covers:
- session creation
- first interact (kind='writing') → student turn + AI invitation, dev_state populated
- second interact (kind='answer') → dev_state evolves, invitation is not identical,
  and an 'answer' is NOT misread as a new draft
- revise flow bug fix: after a genuine kind='revise' with different content, the
  coach acknowledges the change and does NOT claim the student has not revised
- GET session persistence
- empty content → 400
"""
import os
import time

import pytest
import requests

BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/") if os.environ.get(
    "REACT_APP_BACKEND_URL"
) else "https://dev-converse.preview.emergentagent.com"
API = f"{BASE_URL}/api"

# Generous timeout: Claude calls can take up to ~30s
LLM_TIMEOUT = 90


@pytest.fixture(scope="module")
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def created_session(client):
    """Create a session used across tests in this module."""
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
    assert "id" in data and isinstance(data["id"], str) and len(data["id"]) > 0
    assert data["assignment"] == payload["assignment"]
    assert data["pedagogical_purpose"] == payload["pedagogical_purpose"]
    assert data["current_writing_task"] == payload["current_writing_task"]
    assert data["turns"] == []
    # dev_state present with expected default keys
    ds = data["dev_state"]
    for k in [
        "primary_developmental_tension",
        "selected_scaffold",
        "selection_basis",
        "organization_relative_to_purpose",
        "uncertainties",
        "alternative_interpretations",
        "developmental_movement",
    ]:
        assert k in ds
    # empty defaults
    assert ds["primary_developmental_tension"] == ""
    assert ds["selected_scaffold"] == ""
    return data


# ---------------------------------------------------------------------------
# Session creation
# ---------------------------------------------------------------------------
class TestSessionCreation:
    def test_create_session_returns_id_and_empty_state(self, created_session):
        assert created_session["turns"] == []
        assert isinstance(created_session["dev_state"], dict)


# ---------------------------------------------------------------------------
# Interact flow — first writing turn
# ---------------------------------------------------------------------------
class TestFirstInteract:
    """First interact should populate dev_state and return an AI invitation."""

    def test_first_interact_writing(self, client, created_session):
        payload = {
            "kind": "writing",
            "content": (
                "Cars are bad. They cause pollution. Also they cause traffic. "
                "Also they are noisy. I think downtown should ban them because "
                "of these reasons. Downtown is where people live and work so "
                "it is important to make it nice."
            ),
        }
        r = client.post(
            f"{API}/sessions/{created_session['id']}/interact",
            json=payload,
            timeout=LLM_TIMEOUT,
        )
        assert r.status_code == 200, r.text
        data = r.json()
        # persist for next tests
        pytest.first_interact_response = data

        # exactly two turns: student then AI
        assert len(data["turns"]) == 2
        assert data["turns"][0]["role"] == "student"
        assert data["turns"][0]["kind"] == "writing"
        assert data["turns"][1]["role"] == "ai"
        assert data["turns"][1]["kind"] == "invitation"
        invitation = data["turns"][1]["content"].strip()
        assert len(invitation) > 0
        # Should NOT be a rewrite of the essay — a rough heuristic: invitation
        # shouldn't contain most of the student's paragraph verbatim.
        assert "Cars are bad. They cause pollution." not in invitation, (
            "AI appears to be rewriting the student's paragraph"
        )
        # Should NOT be a numbered list of errors
        assert not (invitation.startswith("1.") and "2." in invitation and "3." in invitation), (
            "AI is producing a numbered list of errors instead of a single invitation"
        )

        # dev_state populated
        ds = data["dev_state"]
        assert ds["primary_developmental_tension"].strip() != ""
        assert ds["selected_scaffold"].strip() != ""
        assert ds["selection_basis"].strip() != ""
        assert ds["organization_relative_to_purpose"].strip() != ""
        assert len(ds["uncertainties"]) >= 0  # list present
        assert isinstance(ds["alternative_interpretations"], list)


# ---------------------------------------------------------------------------
# Interact flow — second turn should evolve dev_state and produce new invitation
# ---------------------------------------------------------------------------
class TestSecondInteract:
    def test_second_interact_evolves_state(self, client, created_session):
        first = getattr(pytest, "first_interact_response", None)
        assert first is not None, "First interact must run before this test"

        first_invitation = first["turns"][1]["content"].strip()
        first_movement = first["dev_state"].get("developmental_movement", "").strip().lower()

        payload = {
            "kind": "answer",
            "content": (
                "I think my main claim is that banning cars would make downtown "
                "more livable — cleaner air, safer streets, and better for local "
                "shops because people walk more. My paragraphs weren't organized "
                "around that; I just listed problems. I want to restructure so "
                "each paragraph advances that livability claim."
            ),
        }
        r = client.post(
            f"{API}/sessions/{created_session['id']}/interact",
            json=payload,
            timeout=LLM_TIMEOUT,
        )
        assert r.status_code == 200, r.text
        data = r.json()

        # now 4 turns
        assert len(data["turns"]) == 4
        assert data["turns"][2]["role"] == "student"
        assert data["turns"][2]["kind"] == "answer"
        assert data["turns"][3]["role"] == "ai"
        assert data["turns"][3]["kind"] == "invitation"

        second_invitation = data["turns"][3]["content"].strip()
        assert second_invitation != first_invitation, (
            "Second AI invitation is identical to the first — engine is not "
            "responding to updated interaction."
        )

        # developmental_movement should NOT still say 'initial' after a turn
        movement = data["dev_state"].get("developmental_movement", "").strip().lower()
        assert movement != "", "developmental_movement is empty after 2nd turn"
        assert movement != "initial", (
            f"developmental_movement is still 'initial' after 2nd turn: {movement!r}"
        )

        # Regression: answer must NOT be misread as a new draft. The dev_state
        # 'current_student_writing' should still describe the ORIGINAL draft
        # (the first writing turn), not the answer text. We check that key
        # phrases that only appear in the answer are not lifted into
        # current_student_writing as though they were the draft.
        csw = data["dev_state"].get("current_student_writing", "").lower()
        # The answer is meta-commentary; if csw quotes it verbatim as the draft
        # we'd expect the "livability" framing to show up as if it were in the
        # essay. This is a soft check — we only fail if csw explicitly claims
        # the student HAS restructured / revised (which they haven't yet).
        assert "restructured" not in csw and "has revised" not in csw, (
            f"Answer appears to have been misread as a new draft in "
            f"current_student_writing: {csw!r}"
        )

        pytest.second_interact_response = data


# ---------------------------------------------------------------------------
# Bug fix: revise turn with changed content must be acknowledged
# ---------------------------------------------------------------------------
class TestReviseAcknowledgement:
    """After a genuine revision the coach must NOT claim the student has not revised."""

    def test_revise_is_recognized_as_a_revision(self, client, created_session):
        prior = getattr(pytest, "second_interact_response", None)
        assert prior is not None, "Second interact must run before this test"

        # A meaningfully different draft — restructured around a single
        # 'livability' claim, referencing shops/walking/air.
        revised_draft = (
            "Banning cars from downtown would make the core dramatically more "
            "livable, and every part of my argument hangs from that single "
            "claim. First, air quality: without tailpipe exhaust concentrated "
            "in a few blocks, the people who work and live downtown breathe "
            "cleaner air every day, which is the most basic condition of a "
            "livable place.\n\n"
            "Second, foot traffic and small shops: when streets are for "
            "people, walkers linger, and local businesses that depend on "
            "casual browsing — bookstores, cafes, produce stands — actually "
            "survive. Each of these follows from the livability claim; I am "
            "no longer just listing complaints about cars."
        )
        r = client.post(
            f"{API}/sessions/{created_session['id']}/interact",
            json={"kind": "revise", "content": revised_draft},
            timeout=LLM_TIMEOUT,
        )
        assert r.status_code == 200, r.text
        data = r.json()

        # now 6 turns (2 writing/inv + 2 answer/inv + 2 revise/inv)
        assert len(data["turns"]) == 6
        assert data["turns"][4]["role"] == "student"
        assert data["turns"][4]["kind"] == "revise"
        assert data["turns"][5]["role"] == "ai"
        assert data["turns"][5]["kind"] == "invitation"

        invitation = data["turns"][5]["content"].strip()
        lower_inv = invitation.lower()

        # PRIMARY BUG ASSERTION: the coach must NOT deny the revision.
        deny_phrases = [
            "haven't revised",
            "have not revised",
            "haven't yet revised",
            "have not yet revised",
            "you didn't revise",
            "you did not revise",
            "no revision",
            "no changes",
            "hasn't changed",
            "has not changed",
            "still the same draft",
            "same as before",
            "identical to your previous",
        ]
        for phrase in deny_phrases:
            assert phrase not in lower_inv, (
                f"Coach denied the revision with phrase {phrase!r} in "
                f"invitation: {invitation!r}"
            )

        # And developmental_movement should reflect the change — it must not
        # be empty and must not still be 'initial'.
        movement = data["dev_state"].get("developmental_movement", "").strip().lower()
        assert movement != "", "developmental_movement is empty after revise turn"
        assert movement != "initial", (
            f"developmental_movement is still 'initial' after revise: {movement!r}"
        )
        # It should NOT claim there is no change.
        for phrase in ["no change", "no revision", "unchanged", "identical"]:
            assert phrase not in movement, (
                f"developmental_movement denies the revision: {movement!r}"
            )

        # current_student_writing should reflect the NEW draft's content
        # (livability framing) rather than the original list-of-complaints.
        csw = data["dev_state"].get("current_student_writing", "").lower()
        assert csw.strip() != "", "current_student_writing empty after revise"

        pytest.revise_response = data


# ---------------------------------------------------------------------------
# Persistence: GET returns session with all turns
# ---------------------------------------------------------------------------
class TestPersistence:
    def test_get_session_returns_persisted_turns(self, client, created_session):
        r = client.get(f"{API}/sessions/{created_session['id']}", timeout=30)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["id"] == created_session["id"]
        assert len(data["turns"]) == 6
        # AI invitation strings preserved
        assert data["turns"][1]["role"] == "ai"
        assert data["turns"][3]["role"] == "ai"
        assert data["turns"][5]["role"] == "ai"
        # dev_state persisted
        assert data["dev_state"]["primary_developmental_tension"].strip() != ""

    def test_get_missing_session_returns_404(self, client):
        r = client.get(f"{API}/sessions/does-not-exist-{int(time.time())}", timeout=15)
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# Validation: empty content -> 400
# ---------------------------------------------------------------------------
class TestValidation:
    def test_empty_content_returns_400(self, client, created_session):
        r = client.post(
            f"{API}/sessions/{created_session['id']}/interact",
            json={"kind": "writing", "content": "   "},
            timeout=15,
        )
        assert r.status_code == 400, r.text
