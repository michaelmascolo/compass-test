import { useState, useEffect, useCallback, useRef } from "react";
import "@/App.css";
import { Toaster, toast } from "sonner";
import TeacherSetup from "@/components/TeacherSetup";
import StudentWorkspace from "@/components/StudentWorkspace";
import DevelopmentPanel from "@/components/DevelopmentPanel";
import TestHarness from "@/components/TestHarness";
import { createSession, getSession, interact, editTelos } from "@/lib/api";

const STORAGE_KEY = "dws_session_id";

// Preset teacher context so testers can skip Teacher Setup and start writing immediately.
const TEST_PRESET = {
  assignment: "Argue whether social media improves or harms teen friendships.",
  assignment_prompt:
    "Does social media improve or harm teen friendships? Take a clear position and defend it.",
  pedagogical_purpose:
    "Help the student form and clarify a central claim that organizes the essay, and understand what each part of the writing is doing for the reader.",
  current_writing_task: "Draft your essay.",
  teacher_notes: "",
};

function App() {
  // Developer-only automated instructional testing harness (?tests). Decided at
  // the top-level wrapper so hook order in the studio app is never affected.
  if (new URLSearchParams(window.location.search).has("tests")) {
    return <TestHarness />;
  }
  return <StudioApp />;
}

function StudioApp() {
  const [session, setSession] = useState(null);
  const [booting, setBooting] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [savingTelos, setSavingTelos] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);
  const notifiedFailRef = useRef(new Set());

  // A turn is being reasoned on in the background whenever any turn is "processing".
  const isProcessing = !!session?.turns?.some((t) => t.status === "processing");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const wantsDev = params.has("dev");
    const manualSetup = sessionStorage.getItem("dws_manual_setup") === "1";
    const id = localStorage.getItem(STORAGE_KEY);
    if (!id) {
      // Only auto-load the sample via ?dev if the teacher has NOT explicitly
      // chosen to set up a new assignment (prevents silently restoring the default).
      if (wantsDev && !manualSetup) {
        handleQuickStart().finally(() => setBooting(false));
        return;
      }
      setBooting(false);
      return;
    }
    getSession(id)
      .then(setSession)
      .catch(() => localStorage.removeItem(STORAGE_KEY))
      .finally(() => setBooting(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // The database is the source of truth. Whenever a turn is being reasoned on
  // in the background, poll the session until it completes (or fails). This
  // survives reloads, disconnects, and slow (>180s) reasoning — on reconnect the
  // completed turn is simply loaded from the DB.
  useEffect(() => {
    if (!session?.id || !isProcessing) return;
    const id = session.id;
    let cancelled = false;
    const timer = setInterval(async () => {
      try {
        const s = await getSession(id);
        if (cancelled) return;
        setSession(s);
        const lastAi = [...(s.turns || [])].reverse().find((t) => t.role === "ai");
        if (lastAi && lastAi.status === "failed" && !notifiedFailRef.current.has(lastAi.id)) {
          notifiedFailRef.current.add(lastAi.id);
          toast.error("The coach couldn't respond. Please send your writing again.");
        }
      } catch (e) {
        // transient network error — keep polling; the DB still holds the work
      }
    }, 2500);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [session?.id, isProcessing]);

  const handleBegin = async (form) => {
    setSubmitting(true);
    try {
      const s = await createSession(form);
      localStorage.setItem(STORAGE_KEY, s.id);
      setSession(s);
    } catch (e) {
      toast.error("Could not start the session. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleQuickStart = useCallback(async () => {
    setSubmitting(true);
    try {
      sessionStorage.removeItem("dws_manual_setup");
      const s = await createSession(TEST_PRESET);
      localStorage.setItem(STORAGE_KEY, s.id);
      setSession(s);
    } catch (e) {
      toast.error("Could not start the test session. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }, []);

  // Explicit "Reset to sample assignment" — never silent.
  const handleNewSession = useCallback(async () => {
    localStorage.removeItem(STORAGE_KEY);
    setSession(null);
    await handleQuickStart();
  }, [handleQuickStart]);

  // Go to Teacher Setup for a fresh custom assignment WITHOUT restoring the sample.
  const handleNewAssignment = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    sessionStorage.setItem("dws_manual_setup", "1");
    setSession(null);
  }, []);

  const handleBeginWrapped = useCallback(
    async (form) => {
      sessionStorage.removeItem("dws_manual_setup");
      await handleBegin(form);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const handleSubmit = useCallback(
    async (kind, content) => {
      if (!session) return;
      setSubmitting(true);
      try {
        const updated = await interact(session.id, { kind, content });
        setSession(updated); // now holds a "processing" placeholder; polling takes over
      } catch (e) {
        const msg =
          e?.response?.data?.detail ||
          e?.detail ||
          "The coach could not respond. Please try again.";
        toast.error(msg);
      } finally {
        setSubmitting(false);
      }
    },
    [session]
  );

  const handleEditTelos = useCallback(
    async (form) => {
      if (!session) return;
      setSavingTelos(true);
      try {
        const updated = await editTelos(session.id, form);
        setSession(updated);
        toast.success("Telos revised.");
      } catch (e) {
        toast.error("Could not save the telos. Please try again.");
      } finally {
        setSavingTelos(false);
      }
    },
    [session]
  );

  if (booting) {
    return (
      <div className="min-h-screen paper-grain flex items-center justify-center">
        <p className="font-serif-display text-2xl text-stone-400">
          Opening the studio…
        </p>
      </div>
    );
  }

  return (
    <div className="App">
      <Toaster position="top-center" richColors />
      {!session ? (
        <TeacherSetup
          onBegin={handleBeginWrapped}
          submitting={submitting}
          onQuickStart={handleQuickStart}
        />
      ) : (
        <>
          <StudentWorkspace
            session={session}
            onSubmit={handleSubmit}
            loading={submitting || isProcessing}
            onOpenPanel={() => setPanelOpen(true)}
            onNewSession={handleNewSession}
            onNewAssignment={handleNewAssignment}
          />
          <DevelopmentPanel
            open={panelOpen}
            onClose={() => setPanelOpen(false)}
            session={session}
            onEditTelos={handleEditTelos}
            savingTelos={savingTelos}
          />
        </>
      )}
    </div>
  );
}

export default App;
