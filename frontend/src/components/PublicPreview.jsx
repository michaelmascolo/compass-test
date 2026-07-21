import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Loader2, Compass } from "lucide-react";
import { startPreview, getSession, interact } from "@/lib/api";
import PreviewBridge from "@/components/PreviewBridge";

const PASSAGE_TYPES = ["Let Compass infer it", "Introduction", "Body paragraph", "Transition", "Conclusion", "Other"];

// A single conversational surface. Fully in character: no assignment header,
// no scoring, no jargon, no developer panel. The whole experience is the
// writing invitation and the exchange that follows.
export default function PublicPreview() {
  const [session, setSession] = useState(null);
  const [seed, setSeed] = useState("");
  const [reply, setReply] = useState("");
  const [starting, setStarting] = useState(false);
  const [sending, setSending] = useState(false);
  const [showBridge, setShowBridge] = useState(false);
  const [passageType, setPassageType] = useState("Let Compass infer it");
  const [essayAbout, setEssayAbout] = useState("");
  const threadRef = useRef(null);

  const isProcessing = !!session?.turns?.some((t) => t.status === "processing");
  const busy = starting || sending || isProcessing;

  const turns = (session?.turns || []).filter(
    (t) => !(t.role === "ai" && (t.status === "processing" || t.status === "failed"))
  );
  const started = !!session;
  const aiTurnCount = turns.filter((t) => t.role === "ai").length;
  // Offer a gentle exit once the visitor has genuinely experienced the method.
  const canBridge = aiTurnCount >= 2;

  // Poll while the engine is reasoning in the background.
  useEffect(() => {
    if (!session?.id || !isProcessing) return;
    const id = session.id;
    let cancelled = false;
    const timer = setInterval(async () => {
      try {
        const s = await getSession(id);
        if (!cancelled) setSession(s);
      } catch (e) {
        /* transient — keep polling */
      }
    }, 1500);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [session?.id, isProcessing]);

  useEffect(() => {
    if (threadRef.current) threadRef.current.scrollTop = threadRef.current.scrollHeight;
  }, [turns.length, busy]);

  const beginPreview = useCallback(async () => {
    if (!seed.trim() || starting) return;
    setStarting(true);
    try {
      const s = await startPreview({ essay_about: essayAbout.trim(), passage_type: passageType });
      const updated = await interact(s.id, { kind: "writing", content: seed.trim() });
      setSession(updated);
    } catch (e) {
      setStarting(false);
    } finally {
      setStarting(false);
    }
  }, [seed, starting, essayAbout, passageType]);

  const sendReply = useCallback(async () => {
    if (!reply.trim() || busy || !session) return;
    setSending(true);
    const content = reply.trim();
    setReply("");
    try {
      const updated = await interact(session.id, { kind: "answer", content });
      setSession(updated);
    } catch (e) {
      /* ignore; polling / retry */
    } finally {
      setSending(false);
    }
  }, [reply, busy, session]);

  if (showBridge) {
    return <PreviewBridge sessionId={session?.id} onBack={() => setShowBridge(false)} />;
  }

  return (
    <div className="min-h-screen paper-grain flex flex-col items-center">
      <header className="w-full max-w-2xl flex items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2 font-serif-display text-lg text-stone-800">
          <Compass className="h-5 w-5 text-[#8C3A2A]" />
          Compass
        </div>
        {canBridge && (
          <button
            onClick={() => setShowBridge(true)}
            data-testid="preview-bring-own-work"
            className="text-xs font-mono-panel uppercase tracking-[0.16em] text-stone-500 hover:text-[#8C3A2A] transition-colors"
          >
            Bring your own writing →
          </button>
        )}
      </header>

      <main className="w-full max-w-2xl flex-1 flex flex-col px-6 pb-10">
        {!started ? (
          <SeedScreen
            seed={seed}
            setSeed={setSeed}
            onBegin={beginPreview}
            starting={starting}
            passageType={passageType}
            setPassageType={setPassageType}
            essayAbout={essayAbout}
            setEssayAbout={setEssayAbout}
          />
        ) : (
          <>
            <div
              ref={threadRef}
              className="flex-1 overflow-y-auto custom-scroll py-6 space-y-6"
              data-testid="preview-thread"
            >
              <AnimatePresence initial={false}>
                {turns.map((t) => (
                  <Message key={t.id} turn={t} />
                ))}
              </AnimatePresence>
              {busy && <Thinking />}
            </div>

            <div className="pt-3 border-t border-stone-200">
              <div className="flex items-end gap-2">
                <textarea
                  data-testid="preview-reply-input"
                  value={reply}
                  onChange={(e) => setReply(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      sendReply();
                    }
                  }}
                  rows={2}
                  disabled={busy}
                  placeholder="Type your reply…"
                  className="flex-1 bg-white border border-stone-300 rounded-sm p-3.5 text-[15px] leading-relaxed text-stone-900 placeholder:text-stone-400 outline-none focus:ring-1 focus:ring-stone-900 focus:border-stone-900 transition-colors resize-none disabled:opacity-60"
                />
                <button
                  onClick={sendReply}
                  data-testid="preview-send-button"
                  disabled={!reply.trim() || busy}
                  className="shrink-0 inline-flex items-center gap-2 bg-[#8C3A2A] text-white px-5 py-3.5 rounded-sm font-medium hover:bg-[#6B2C20] enabled:hover:-translate-y-px transition-[background-color,transform] disabled:opacity-40 disabled:cursor-not-allowed"
                  aria-label="Send"
                >
                  {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

function SeedScreen({ seed, setSeed, onBegin, starting, passageType, setPassageType, essayAbout, setEssayAbout }) {
  const empty = !seed.trim();
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="flex-1 flex flex-col justify-center max-w-xl mx-auto w-full py-10"
      data-testid="preview-seed-screen"
    >
      <h1 className="font-serif-display text-3xl sm:text-4xl leading-snug text-stone-900">
        Try Compass with a short piece of Grade 9 writing.
      </h1>
      <p className="text-stone-600 mt-4 text-[15px] leading-relaxed">
        Choose any essay topic. Write or paste a short passage as though it were part of a Grade 9
        student’s essay. You might enter an introduction, a body paragraph, a transition, or a
        conclusion.
      </p>
      <p className="text-stone-500 mt-2 text-[14px] leading-relaxed">
        The writing can be imperfect. The purpose is to experience how Compass helps a student
        develop it.
      </p>

      {/* Optional essay context */}
      <div className="mt-7">
        <label className="block font-mono-panel text-[11px] uppercase tracking-[0.14em] text-stone-500 mb-1.5">
          What is the essay about? <span className="text-stone-400 normal-case tracking-normal">Optional</span>
        </label>
        <input
          data-testid="preview-essay-about"
          value={essayAbout}
          onChange={(e) => setEssayAbout(e.target.value)}
          placeholder="Briefly describe the topic or assignment."
          className="w-full bg-white border border-stone-300 rounded-sm px-3.5 py-2.5 text-[15px] text-stone-900 placeholder:text-stone-400 outline-none focus:ring-1 focus:ring-[#8C3A2A] focus:border-[#8C3A2A] transition-colors"
        />
      </div>

      {/* Optional passage type */}
      <div className="mt-4">
        <label className="block font-mono-panel text-[11px] uppercase tracking-[0.14em] text-stone-500 mb-1.5">
          What kind of passage are you entering? <span className="text-stone-400 normal-case tracking-normal">Optional</span>
        </label>
        <select
          data-testid="preview-passage-type"
          value={passageType}
          onChange={(e) => setPassageType(e.target.value)}
          className="w-full bg-white border border-stone-300 rounded-sm px-3.5 py-2.5 text-[15px] text-stone-900 outline-none focus:ring-1 focus:ring-[#8C3A2A] focus:border-[#8C3A2A] transition-colors"
        >
          {PASSAGE_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      <textarea
        data-testid="preview-seed-input"
        value={seed}
        onChange={(e) => setSeed(e.target.value)}
        rows={7}
        autoFocus
        placeholder="Enter a short passage here…"
        className="mt-5 w-full bg-white border border-stone-300 rounded-sm p-5 text-[16px] leading-8 text-stone-900 placeholder:text-stone-400 outline-none focus:ring-1 focus:ring-stone-900 focus:border-stone-900 transition-colors resize-none"
      />
      <button
        onClick={onBegin}
        data-testid="preview-begin-button"
        disabled={empty || starting}
        className="mt-5 self-start group inline-flex items-center gap-2 bg-[#8C3A2A] text-white px-7 py-3 rounded-sm font-medium tracking-wide hover:bg-[#6B2C20] enabled:hover:-translate-y-px transition-[background-color,transform] disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {starting ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            Reading…
          </>
        ) : (
          <>
            Try Compass
            <ArrowRight className="h-4 w-4 transition-transform group-enabled:group-hover:translate-x-0.5" />
          </>
        )}
      </button>
      {empty && (
        <span className="text-stone-400 text-[13px] mt-2" data-testid="preview-empty-hint">
          Enter a short passage to continue.
        </span>
      )}
    </motion.div>
  );
}

function Message({ turn }) {
  const isAI = turn.role === "ai";
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={isAI ? "flex justify-start" : "flex justify-end"}
      data-testid={isAI ? "preview-coach-message" : "preview-user-message"}
    >
      {isAI ? (
        <p className="max-w-[90%] text-stone-800 leading-relaxed text-[17px] font-serif-display whitespace-pre-wrap">
          {turn.content}
        </p>
      ) : (
        <p className="max-w-[85%] bg-stone-900 text-stone-100 rounded-sm px-4 py-2.5 leading-relaxed text-[15px] whitespace-pre-wrap">
          {turn.content}
        </p>
      )}
    </motion.div>
  );
}

function Thinking() {
  const lines = [
    "Reading your opening as a reader would…",
    "Sitting with what you actually said…",
    "Thinking about what a reader needs here…",
  ];
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((n) => (n + 1) % lines.length), 4000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div className="flex items-center gap-3 pl-1" data-testid="preview-thinking">
      <div className="flex items-center gap-1.5">
        <span className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]" />
        <span className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]" style={{ animationDelay: "0.2s" }} />
        <span className="thinking-dot h-2 w-2 rounded-full bg-[#8C3A2A]" style={{ animationDelay: "0.4s" }} />
      </div>
      <motion.span
        key={i}
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.7 }}
        transition={{ duration: 0.6 }}
        className="text-stone-500 text-sm italic font-serif-display"
      >
        {lines[i]}
      </motion.span>
    </div>
  );
}
