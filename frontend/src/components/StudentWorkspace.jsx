import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Loader2,
  MessageSquareQuote,
  Send,
  FlaskConical,
  BookOpen,
  RotateCcw,
} from "lucide-react";

function ThreadBubble({ turn }) {
  const isAI = turn.role === "ai";
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={isAI ? "" : "flex justify-end"}
      data-testid={isAI ? "ai-invitation" : "student-turn"}
    >
      {isAI ? (
        <div className="bg-white border border-stone-200 rounded-sm p-4">
          <div className="flex items-center gap-1.5 text-[10px] uppercase tracking-[0.18em] text-[#8C3A2A] font-mono-panel mb-2">
            <MessageSquareQuote className="h-3.5 w-3.5" />
            Developmental invitation
          </div>
          <p className="text-stone-800 leading-relaxed text-[15px] whitespace-pre-wrap">
            {turn.content}
          </p>
        </div>
      ) : (
        <div className="max-w-[88%] bg-stone-900 text-stone-100 rounded-sm p-3.5">
          <div className="text-[10px] uppercase tracking-[0.18em] text-stone-400 font-mono-panel mb-1">
            You · {turn.kind}
          </div>
          <p className="leading-relaxed text-sm whitespace-pre-wrap">
            {turn.content}
          </p>
        </div>
      )}
    </motion.div>
  );
}

export default function StudentWorkspace({
  session,
  onSubmit,
  loading,
  onOpenPanel,
  onNewSession,
}) {
  const [draft, setDraft] = useState("");
  const [reply, setReply] = useState("");
  const [replyMode, setReplyMode] = useState("answer");
  const threadRef = useRef(null);

  const allTurns = session.turns || [];
  // Only render completed exchanges; the in-flight placeholder and failed turns
  // are represented by the thinking indicator / a toast instead.
  const turns = allTurns.filter(
    (t) => !(t.role === "ai" && (t.status === "processing" || t.status === "failed"))
  );
  const started = allTurns.some((t) => t.role === "student");

  useEffect(() => {
    if (threadRef.current) {
      threadRef.current.scrollTop = threadRef.current.scrollHeight;
    }
  }, [turns.length, loading]);

  const submitDraft = () => {
    if (!draft.trim() || loading) return;
    onSubmit(started ? "revise" : "writing", draft.trim());
  };

  const submitReply = () => {
    if (!reply.trim() || loading) return;
    onSubmit(replyMode, reply.trim());
    setReply("");
  };

  return (
    <div className="min-h-screen paper-grain flex flex-col">
      {/* top bar */}
      <header className="flex items-center justify-between px-6 sm:px-10 py-4 border-b border-stone-200 bg-[#faf9f6]/90 backdrop-blur-sm sticky top-0 z-20">
        <div className="flex items-center gap-2 font-serif-display text-xl text-stone-900">
          <BookOpen className="h-5 w-5 text-[#8C3A2A]" />
          Writing Studio
        </div>
        <div className="flex items-center gap-2">
          {onNewSession && (
            <button
              onClick={() => !loading && onNewSession()}
              disabled={loading}
              data-testid="new-test-session-button"
              className="inline-flex items-center gap-1.5 text-xs font-mono-panel uppercase tracking-[0.15em] text-stone-500 hover:text-[#8C3A2A] border border-stone-300 hover:border-[#8C3A2A] rounded-sm px-3 py-1.5 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              New Test
            </button>
          )}
          <button
            onClick={onOpenPanel}
            data-testid="open-dev-panel-button"
            className="inline-flex items-center gap-1.5 text-xs font-mono-panel uppercase tracking-[0.15em] text-stone-500 hover:text-stone-900 border border-stone-300 hover:border-stone-900 rounded-sm px-3 py-1.5 transition-colors"
          >
            <FlaskConical className="h-3.5 w-3.5" />
            Dev Panel
          </button>
        </div>
      </header>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12">
        {/* Canvas */}
        <section className="lg:col-span-7 xl:col-span-8 border-r border-stone-200 flex flex-col">
          <div className="px-6 sm:px-12 pt-10 pb-6">
            <p className="font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-500">
              Assignment
            </p>
            <h1 className="font-serif-display text-2xl sm:text-3xl tracking-tight text-stone-900 mt-1 leading-snug">
              {session.assignment}
            </h1>
            <div className="mt-4 border-l-2 border-[#8C3A2A] pl-4">
              <p className="font-mono-panel text-[10px] uppercase tracking-[0.2em] text-[#8C3A2A]">
                Current Writing Task
              </p>
              <p className="text-stone-700 mt-1 leading-relaxed">
                {session.current_writing_task}
              </p>
            </div>
          </div>

          <div className="px-6 sm:px-12 pb-10 flex-1 flex flex-col">
            <label
              htmlFor="draft"
              className="font-mono-panel text-[10px] uppercase tracking-[0.2em] text-stone-500 mb-2"
            >
              {started ? "Your draft — revise or keep writing" : "Your writing"}
            </label>
            <textarea
              id="draft"
              data-testid="writing-area"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="Begin writing here. Take your time — write what you actually think, then send it to the coach."
              className="flex-1 min-h-[320px] w-full bg-white border border-stone-300 rounded-sm p-6 text-[17px] leading-8 text-stone-900 placeholder:text-stone-400 outline-none focus:ring-1 focus:ring-stone-900 focus:border-stone-900 transition-colors resize-none custom-scroll font-serif-display"
            />
            <div className="mt-4 flex items-center justify-between">
              <span className="text-xs text-stone-500 font-mono-panel">
                {draft.trim() ? draft.trim().split(/\s+/).length : 0} words
              </span>
              <button
                onClick={submitDraft}
                data-testid="continue-button"
                disabled={!draft.trim() || loading}
                className="group inline-flex items-center gap-2 bg-[#8C3A2A] text-white px-6 py-3 rounded-sm font-medium tracking-wide hover:bg-[#6B2C20] enabled:hover:-translate-y-px transition-[background-color,transform] disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Reading…
                  </>
                ) : (
                  <>
                    {started ? "Send revised draft" : "Continue"}
                    <ArrowRight className="h-4 w-4 transition-transform group-enabled:group-hover:translate-x-0.5" />
                  </>
                )}
              </button>
            </div>
          </div>
        </section>

        {/* Scaffold thread */}
        <aside className="lg:col-span-5 xl:col-span-4 flex flex-col bg-stone-50/60 h-[calc(100vh-65px)] sticky top-[65px]">
          <div className="px-6 py-4 border-b border-stone-200 shrink-0">
            <p className="font-serif-display text-lg text-stone-900">
              Conversation with your coach
            </p>
            <p className="text-xs text-stone-500 mt-0.5">
              One focused invitation at a time.
            </p>
          </div>

          <div
            ref={threadRef}
            className="flex-1 overflow-y-auto custom-scroll px-5 py-5 space-y-4"
            data-testid="conversation-thread"
          >
            {!started && (
              <div className="h-full flex items-center justify-center text-center px-6">
                <p className="text-stone-400 leading-relaxed text-sm">
                  Send your first piece of writing and the coach will respond
                  with a single developmental invitation.
                </p>
              </div>
            )}
            {turns.map((t) => (
              <ThreadBubble key={t.id} turn={t} />
            ))}
            {loading && (
              <div className="flex items-center gap-1.5 pl-1">
                <span className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]" />
                <span
                  className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]"
                  style={{ animationDelay: "0.2s" }}
                />
                <span
                  className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]"
                  style={{ animationDelay: "0.4s" }}
                />
              </div>
            )}
          </div>

          {started && (
            <div className="border-t border-stone-200 p-4 shrink-0 bg-white">
              <div className="flex gap-2 mb-2">
                {["answer", "explain", "revise"].map((m) => (
                  <button
                    key={m}
                    data-testid={`reply-mode-${m}`}
                    onClick={() => setReplyMode(m)}
                    className={`text-[11px] font-mono-panel uppercase tracking-[0.15em] px-3 py-1 rounded-sm border transition-colors ${
                      replyMode === m
                        ? "bg-stone-900 text-white border-stone-900"
                        : "bg-transparent text-stone-500 border-stone-300 hover:border-stone-900"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
              <div className="flex items-end gap-2">
                <textarea
                  data-testid="reply-input"
                  value={reply}
                  onChange={(e) => setReply(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && (e.metaKey || e.ctrlKey))
                      submitReply();
                  }}
                  rows={2}
                  placeholder={
                    replyMode === "answer"
                      ? "Answer the coach's question…"
                      : replyMode === "explain"
                        ? "Explain your thinking…"
                        : "Paste or type your revised writing…"
                  }
                  className="flex-1 bg-white border border-stone-300 rounded-sm p-3 text-sm text-stone-900 placeholder:text-stone-400 outline-none focus:ring-1 focus:ring-stone-900 focus:border-stone-900 transition-colors resize-none"
                />
                <button
                  onClick={submitReply}
                  data-testid="send-reply-button"
                  disabled={!reply.trim() || loading}
                  className="shrink-0 bg-[#8C3A2A] text-white p-3 rounded-sm hover:bg-[#6B2C20] enabled:hover:-translate-y-px transition-[background-color,transform] disabled:opacity-40 disabled:cursor-not-allowed"
                  aria-label="Send reply"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
              <p className="text-[10px] text-stone-400 mt-1.5">
                Revise here with the <span className="font-medium">revise</span> mode, or edit your draft on the left and send it again.
              </p>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
