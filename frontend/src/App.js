import { useState, useEffect, useCallback } from "react";
import "@/App.css";
import { Toaster, toast } from "sonner";
import TeacherSetup from "@/components/TeacherSetup";
import StudentWorkspace from "@/components/StudentWorkspace";
import DevelopmentPanel from "@/components/DevelopmentPanel";
import { createSession, getSession, interact, editTelos } from "@/lib/api";

const STORAGE_KEY = "dws_session_id";

function App() {
  const [session, setSession] = useState(null);
  const [booting, setBooting] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [savingTelos, setSavingTelos] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);

  useEffect(() => {
    const id = localStorage.getItem(STORAGE_KEY);
    if (!id) {
      setBooting(false);
      return;
    }
    getSession(id)
      .then(setSession)
      .catch(() => localStorage.removeItem(STORAGE_KEY))
      .finally(() => setBooting(false));
  }, []);

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

  const handleSubmit = useCallback(
    async (kind, content) => {
      if (!session) return;
      setSubmitting(true);
      try {
        const updated = await interact(session.id, { kind, content });
        setSession(updated);
      } catch (e) {
        const msg =
          e?.detail ||
          e?.response?.data?.detail ||
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
        <TeacherSetup onBegin={handleBegin} submitting={submitting} />
      ) : (
        <>
          <StudentWorkspace
            session={session}
            onSubmit={handleSubmit}
            loading={submitting}
            onOpenPanel={() => setPanelOpen(true)}
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
