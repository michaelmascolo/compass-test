import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Toaster, toast } from "sonner";
import {
  ArrowRight,
  ArrowLeft,
  Loader2,
  FileText,
  Compass as CompassIcon,
  Pencil,
  CornerDownRight,
  CircleDot,
} from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  createAssignmentSession,
  getAssignmentSession,
  editAssignment,
  submitInterpretation,
  submitOperation,
  submitRestatement,
} from "@/lib/api";

const STORE = "compass_rep_session";

const SAMPLE =
  "Compare fixed and growth mindsets. Explain how each mindset affects both the process and outcomes of learning. Use relevant examples to support your explanation.";

const STATUS_META = {
  understood: { label: "Understood", dot: "#5b7a52", text: "text-[#41603a]", bg: "bg-[#eef2ea]" },
  developing: { label: "Developing", dot: "#b8863b", text: "text-[#8a6524]", bg: "bg-[#f6efe1]" },
  needs_attention: { label: "Needs Attention", dot: "#8C3A2A", text: "text-[#8C3A2A]", bg: "bg-[#f5e6e1]" },
  unconfirmed: { label: "Unconfirmed Requirement", dot: "#a8a29e", text: "text-stone-500", bg: "bg-stone-100" },
};

const meta = (s) => STATUS_META[s] || STATUS_META.unconfirmed;

// ---------------------------------------------------------------------------
function DemandRow({ d, active, flash }) {
  const m = meta(d.status);
  return (
    <motion.div
      layout
      data-testid={`demand-${d.id}`}
      data-status={d.status}
      animate={flash ? { backgroundColor: ["#fff7ed", "#ffffff"] } : {}}
      transition={{ duration: 1.2 }}
      className={`relative rounded-sm bg-white pl-4 pr-3 py-3 ${
        active ? "ring-1 ring-[#8C3A2A]" : ""
      }`}
      style={{
        borderLeft: `3px ${d.source === "inferred" ? "dashed" : "solid"} ${
          active ? "#8C3A2A" : "#d6d3d1"
        }`,
      }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-serif-display text-[15px] leading-snug text-stone-900">
              {d.label}
            </span>
            <span
              className="shrink-0 rounded-sm border border-stone-200 px-1.5 py-px text-[9px] font-mono-panel uppercase tracking-[0.14em] text-stone-400"
              title={d.source === "inferred" ? "Inferred from the task" : "Stated in the assignment"}
            >
              {d.source === "inferred" ? "Inferred" : "Explicit"}
            </span>
          </div>
          {d.operation && (
            <p className="mt-0.5 text-[11px] font-mono-panel uppercase tracking-[0.12em] text-stone-400">
              {d.operation}
            </p>
          )}
        </div>
        <span
          className={`inline-flex shrink-0 items-center gap-1.5 rounded-full px-2 py-1 text-[10px] font-mono-panel uppercase tracking-[0.1em] ${m.bg} ${m.text}`}
        >
          <span className="h-1.5 w-1.5 rounded-full" style={{ background: m.dot }} />
          {m.label}
        </span>
      </div>
      {active && (
        <div className="mt-1.5 inline-flex items-center gap-1 text-[10px] font-mono-panel uppercase tracking-[0.14em] text-[#8C3A2A]">
          <CircleDot className="h-3 w-3" /> Working on this
        </div>
      )}
    </motion.div>
  );
}

function QuestionMap({ session, flashIds }) {
  return (
    <div data-testid="question-map" className="space-y-2.5">
      <p className="mb-1 font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-500">
        What this assignment asks
      </p>
      <AnimatePresence initial={false}>
        {session.demands.map((d) => (
          <DemandRow
            key={d.id}
            d={d}
            active={d.id === session.active_target_id}
            flash={flashIds.has(d.id)}
          />
        ))}
      </AnimatePresence>
      <p className="pt-1 text-[11px] leading-relaxed text-stone-400">
        Solid border = stated in the assignment · dashed = inferred. This map is adequate for now,
        not a permanent checklist.
      </p>
    </div>
  );
}

function AssignmentPanel({ text, onEdit }) {
  return (
    <div className="rounded-sm border border-stone-200 bg-[#faf9f6] p-5">
      <div className="mb-2 flex items-center justify-between">
        <span className="flex items-center gap-1.5 font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-500">
          <FileText className="h-3.5 w-3.5" /> The assignment
        </span>
        {onEdit && (
          <button
            onClick={onEdit}
            data-testid="edit-assignment-button"
            className="inline-flex items-center gap-1 text-[10px] font-mono-panel uppercase tracking-[0.14em] text-stone-400 transition-colors hover:text-[#8C3A2A]"
          >
            <Pencil className="h-3 w-3" /> Edit
          </button>
        )}
      </div>
      <p className="font-serif-display text-[17px] leading-relaxed text-stone-900">{text}</p>
    </div>
  );
}

// ---------------------------------------------------------------------------
export default function AssignmentRepresentation() {
  const [session, setSession] = useState(null);
  const [assignmentText, setAssignmentText] = useState("");
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [booting, setBooting] = useState(true);
  const [editing, setEditing] = useState(false);
  const [restartOpen, setRestartOpen] = useState(false);
  const [knowledge, setKnowledge] = useState(false);
  const prevStatus = useRef({});
  const [flashIds, setFlashIds] = useState(new Set());

  // apply a session update and flash any demands whose status changed
  const applySession = useCallback((s) => {
    const changed = new Set();
    (s.demands || []).forEach((d) => {
      if (prevStatus.current[d.id] && prevStatus.current[d.id] !== d.status) changed.add(d.id);
      prevStatus.current[d.id] = d.status;
    });
    setSession(s);
    setInput("");
    if (changed.size) {
      setFlashIds(changed);
      setTimeout(() => setFlashIds(new Set()), 1400);
    }
  }, []);

  useEffect(() => {
    const id = localStorage.getItem(STORE);
    if (!id) {
      setBooting(false);
      return;
    }
    getAssignmentSession(id)
      .then((s) => {
        (s.demands || []).forEach((d) => (prevStatus.current[d.id] = d.status));
        setSession(s);
      })
      .catch(() => localStorage.removeItem(STORE))
      .finally(() => setBooting(false));
  }, []);

  const runAnalyze = async () => {
    const text = assignmentText.trim();
    if (!text || busy) return;
    setBusy(true);
    try {
      let s;
      if (editing && session) {
        s = await editAssignment(session.id, text);
        toast.success("Assignment updated — analysis restarted.");
      } else {
        s = await createAssignmentSession(text);
      }
      localStorage.setItem(STORE, s.id);
      prevStatus.current = {};
      (s.demands || []).forEach((d) => (prevStatus.current[d.id] = d.status));
      setSession(s);
      setEditing(false);
      setKnowledge(false);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not analyze the assignment.");
    } finally {
      setBusy(false);
    }
  };

  const send = async (fn) => {
    const text = input.trim();
    if (!text || busy) return;
    setBusy(true);
    try {
      const s = await fn(session.id, text);
      applySession(s);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  const startEdit = () => {
    setAssignmentText(session.assignment_text);
    setRestartOpen(true);
  };
  const confirmEdit = () => {
    setEditing(true);
    setRestartOpen(false);
    setSession(null);
  };

  const Thinking = () => (
    <div data-testid="thinking-state" className="flex items-center gap-2 text-sm text-stone-500">
      <Loader2 className="h-4 w-4 animate-spin text-[#8C3A2A]" /> Thinking…
    </div>
  );

  if (booting) {
    return (
      <div className="flex min-h-screen items-center justify-center paper-grain">
        <p className="font-serif-display text-2xl text-stone-400">Opening Compass…</p>
      </div>
    );
  }

  // ============ Knowledge placeholder (Sprint 2 stub) ============
  if (knowledge) {
    return (
      <div className="min-h-screen paper-grain">
        <Header />
        <div className="mx-auto max-w-2xl px-6 py-24 text-center">
          <p className="font-mono-panel text-[11px] uppercase tracking-[0.2em] text-stone-400">
            Next
          </p>
          <h1 className="mt-3 font-serif-display text-4xl text-stone-900">The Knowledge Loop</h1>
          <p className="mx-auto mt-4 max-w-md text-stone-600">
            You've built an adequate representation of what this assignment asks. Gathering and
            organizing what you know comes next — that part of Compass is still being built.
          </p>
          <button
            onClick={() => setKnowledge(false)}
            data-testid="knowledge-back-button"
            className="mt-8 inline-flex items-center gap-2 text-sm text-stone-500 underline underline-offset-4 hover:text-[#8C3A2A]"
          >
            <ArrowLeft className="h-4 w-4" /> Back to the assignment
          </button>
        </div>
      </div>
    );
  }

  // ============ A. Assignment Entry ============
  if (!session) {
    return (
      <div className="min-h-screen paper-grain">
        <Toaster position="top-center" richColors />
        <Header />
        <div className="mx-auto max-w-2xl px-6 py-16">
          <p className="font-mono-panel text-[11px] uppercase tracking-[0.2em] text-[#8C3A2A]">
            {editing ? "Edit assignment" : "Start here"}
          </p>
          <h1 className="mt-3 font-serif-display text-4xl text-stone-900 sm:text-5xl">
            What does this assignment ask of you?
          </h1>
          <p className="mt-4 text-stone-600">
            Paste the assignment. Before gathering ideas or writing, Compass helps you understand
            exactly what it requires.
          </p>
          <textarea
            data-testid="assignment-input"
            value={assignmentText}
            onChange={(e) => setAssignmentText(e.target.value)}
            rows={6}
            placeholder="Paste the full assignment here…"
            className="mt-6 w-full resize-none rounded-sm border border-stone-300 bg-white p-4 font-serif-display text-[17px] leading-relaxed text-stone-900 outline-none focus:border-[#8C3A2A]"
          />
          <div className="mt-4 flex flex-wrap items-center gap-4">
            <button
              onClick={runAnalyze}
              disabled={!assignmentText.trim() || busy}
              data-testid="analyze-assignment-button"
              className="group inline-flex items-center gap-2 rounded-sm bg-[#8C3A2A] px-6 py-3 font-medium tracking-wide text-white transition-colors hover:bg-[#6B2C20] disabled:opacity-40"
            >
              {busy ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Analyzing…
                </>
              ) : (
                <>
                  Analyze assignment
                  <ArrowRight className="h-4 w-4 transition-transform group-enabled:group-hover:translate-x-0.5" />
                </>
              )}
            </button>
            <button
              onClick={() => setAssignmentText(SAMPLE)}
              data-testid="sample-assignment-button"
              className="text-[11px] font-mono-panel uppercase tracking-[0.14em] text-stone-400 transition-colors hover:text-[#8C3A2A]"
            >
              Use sample assignment
            </button>
            {editing && (
              <button
                onClick={() => {
                  setEditing(false);
                  const id = localStorage.getItem(STORE);
                  if (id) getAssignmentSession(id).then(setSession);
                }}
                className="text-[11px] font-mono-panel uppercase tracking-[0.14em] text-stone-400 hover:text-stone-700"
              >
                Cancel
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // ============ B. Student Interpretation ============
  if (session.stage === "interpret") {
    return (
      <div className="min-h-screen paper-grain">
        <Toaster position="top-center" richColors />
        <Header />
        <div className="mx-auto max-w-2xl px-6 py-12">
          <AssignmentPanel text={session.assignment_text} onEdit={startEdit} />
          <div className="mt-8">
            <p className="font-mono-panel text-[11px] uppercase tracking-[0.2em] text-[#8C3A2A]">
              In your own words
            </p>
            <h2 className="mt-2 font-serif-display text-2xl text-stone-900">
              What is this assignment asking you to do?
            </h2>
            <p className="mt-2 text-sm text-stone-600">
              Don't answer the assignment yet. Just explain what it requires, as you understand it.
            </p>
            <textarea
              data-testid="interpretation-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              rows={5}
              placeholder="Explain what the assignment is asking…"
              className="mt-4 w-full resize-none rounded-sm border border-stone-300 bg-white p-4 text-[15px] leading-relaxed text-stone-900 outline-none focus:border-[#8C3A2A]"
            />
            <div className="mt-4 flex items-center gap-4">
              <button
                onClick={() => send(submitInterpretation)}
                disabled={!input.trim() || busy}
                data-testid="compare-understanding-button"
                className="inline-flex items-center gap-2 rounded-sm bg-[#8C3A2A] px-6 py-3 font-medium text-white transition-colors hover:bg-[#6B2C20] disabled:opacity-40"
              >
                {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                Compare my understanding
              </button>
              {busy && <Thinking />}
            </div>
          </div>
        </div>
        <RestartDialog open={restartOpen} setOpen={setRestartOpen} confirm={confirmEdit} />
      </div>
    );
  }

  // ============ C + D + E : two-column working view ============
  const scaffold = session.current_scaffold;
  return (
    <div className="min-h-screen paper-grain">
      <Toaster position="top-center" richColors />
      <Header />
      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-8 px-6 py-10 lg:grid-cols-2">
        {/* LEFT — assignment + persistent Question Map */}
        <div className="space-y-6">
          <AssignmentPanel text={session.assignment_text} onEdit={startEdit} />
          <QuestionMap session={session} flashIds={flashIds} />
        </div>

        {/* RIGHT — active developmental work */}
        <div className="lg:sticky lg:top-6 lg:self-start">
          {session.stage === "mapping" && scaffold && (
            <div data-testid="scaffold-panel" className="rounded-sm border border-stone-200 bg-white p-6">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-sm bg-[#8C3A2A] px-2 py-1 text-[10px] font-mono-panel uppercase tracking-[0.14em] text-white">
                  {scaffold.targetOperation || "Perform"}
                </span>
                {(scaffold.concepts || []).map((c) => (
                  <span
                    key={c}
                    className="rounded-sm border border-stone-200 px-2 py-1 text-[10px] font-mono-panel uppercase tracking-[0.1em] text-stone-500"
                  >
                    {c}
                  </span>
                ))}
              </div>
              {scaffold.relevant_wording && (
                <p className="mt-4 border-l-2 border-stone-300 pl-3 font-serif-display text-[15px] italic text-stone-600">
                  “{scaffold.relevant_wording}”
                </p>
              )}
              <p
                data-testid="scaffold-task"
                className="mt-4 whitespace-pre-wrap text-[16px] leading-relaxed text-stone-900"
              >
                {scaffold.studentTask}
              </p>
              {scaffold.requires_reconstruction && (
                <p className="mt-3 inline-flex items-center gap-1.5 text-[11px] font-mono-panel uppercase tracking-[0.12em] text-[#8C3A2A]">
                  <CornerDownRight className="h-3.5 w-3.5" /> Put this in your own words
                </p>
              )}
              <textarea
                data-testid="operation-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={5}
                placeholder="Write your response…"
                className="mt-4 w-full resize-none rounded-sm border border-stone-300 bg-[#faf9f6] p-3.5 text-[15px] leading-relaxed text-stone-900 outline-none focus:border-[#8C3A2A]"
              />
              <div className="mt-3 flex items-center gap-4">
                <button
                  onClick={() => send(submitOperation)}
                  disabled={!input.trim() || busy}
                  data-testid="submit-operation-button"
                  className="inline-flex items-center gap-2 rounded-sm bg-[#8C3A2A] px-5 py-2.5 font-medium text-white transition-colors hover:bg-[#6B2C20] disabled:opacity-40"
                >
                  {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                  Submit response
                </button>
                {busy && <Thinking />}
              </div>
            </div>
          )}

          {session.stage === "restatement" && (
            <div data-testid="restatement-panel" className="rounded-sm border border-stone-200 bg-white p-6">
              <p className="font-mono-panel text-[11px] uppercase tracking-[0.2em] text-[#8C3A2A]">
                Pull it together
              </p>
              <h2 className="mt-2 font-serif-display text-2xl text-stone-900">
                Explain the whole assignment again, in your own words.
              </h2>
              <p className="mt-2 text-sm text-stone-600">
                Now that you've worked through the parts, restate what this assignment requires — all
                of it.
              </p>
              <textarea
                data-testid="restatement-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={6}
                placeholder="Restate the full assignment…"
                className="mt-4 w-full resize-none rounded-sm border border-stone-300 bg-[#faf9f6] p-3.5 text-[15px] leading-relaxed text-stone-900 outline-none focus:border-[#8C3A2A]"
              />
              <div className="mt-3 flex items-center gap-4">
                <button
                  onClick={() => send(submitRestatement)}
                  disabled={!input.trim() || busy}
                  data-testid="submit-restatement-button"
                  className="inline-flex items-center gap-2 rounded-sm bg-[#8C3A2A] px-5 py-2.5 font-medium text-white transition-colors hover:bg-[#6B2C20] disabled:opacity-40"
                >
                  {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                  Check my representation
                </button>
                {busy && <Thinking />}
              </div>
            </div>
          )}

          {session.stage === "adequate" && (
            <div data-testid="adequate-panel" className="rounded-sm border border-[#5b7a52]/40 bg-[#eef2ea] p-6">
              <p className="font-mono-panel text-[11px] uppercase tracking-[0.2em] text-[#41603a]">
                Adequate for now
              </p>
              <h2 className="mt-2 font-serif-display text-2xl text-stone-900">
                You understand what this assignment requires.
              </h2>
              <p className="mt-2 text-sm text-stone-600">
                Your representation is solid enough to move forward. You can keep refining it later.
              </p>
              <button
                onClick={() => setKnowledge(true)}
                data-testid="continue-to-knowledge-button"
                className="group mt-6 inline-flex items-center gap-2 rounded-sm bg-[#8C3A2A] px-6 py-3 font-medium text-white transition-colors hover:bg-[#6B2C20]"
              >
                Continue to Knowledge
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>
          )}

          {/* Preserved learner responses */}
          {session.interactions?.length > 0 && (
            <div data-testid="response-history" className="mt-6">
              <p className="mb-2 font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-400">
                Your responses
              </p>
              <div className="space-y-2">
                {session.interactions
                  .filter((i) => i.student_text)
                  .map((i, idx) => (
                    <div
                      key={i.id || idx}
                      data-testid={`response-history-item-${idx}`}
                      className="rounded-sm border border-stone-200 bg-white px-3 py-2"
                    >
                      <p className="font-mono-panel text-[9px] uppercase tracking-[0.16em] text-stone-400">
                        {i.kind}
                      </p>
                      <p className="mt-0.5 text-[13px] leading-snug text-stone-600 line-clamp-3">
                        {i.student_text}
                      </p>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      </div>
      <RestartDialog open={restartOpen} setOpen={setRestartOpen} confirm={confirmEdit} />
    </div>
  );
}

function Header() {
  return (
    <header className="flex items-center justify-between border-b border-stone-200 bg-[#faf9f6]/90 px-6 py-4 backdrop-blur-sm sm:px-10">
      <a
        href="/"
        className="flex items-center gap-2 font-serif-display text-lg text-stone-900"
        data-testid="rep-home-link"
      >
        <CompassIcon className="h-5 w-5 text-[#8C3A2A]" />
        Compass
      </a>
      <span className="font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-400">
        Understand the assignment
      </span>
    </header>
  );
}

function RestartDialog({ open, setOpen, confirm }) {
  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogContent data-testid="restart-warning-dialog">
        <AlertDialogHeader>
          <AlertDialogTitle>Edit the assignment and restart?</AlertDialogTitle>
          <AlertDialogDescription>
            Changing the assignment restarts the analysis. Your current Question Map and responses
            for this assignment will be cleared.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel data-testid="restart-cancel">Keep working</AlertDialogCancel>
          <AlertDialogAction
            onClick={confirm}
            data-testid="restart-confirm"
            className="bg-[#8C3A2A] hover:bg-[#6B2C20]"
          >
            Edit &amp; restart
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
