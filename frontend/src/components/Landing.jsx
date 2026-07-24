import { motion } from "framer-motion";
import { Compass, ArrowRight } from "lucide-react";

const go = (query) => {
  window.location.href = `${window.location.pathname}?${query}`;
};

const ease = [0.22, 1, 0.36, 1];
const rise = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease, delay },
});

export default function Landing() {
  return (
    <div className="min-h-screen paper-grain flex flex-col">
      {/* Header */}
      <header
        className="flex items-center justify-between py-6 px-8 md:px-12 border-b border-stone-200 bg-[#faf9f6]"
        data-testid="landing-header"
      >
        <div className="flex items-center gap-2 font-serif-display text-xl text-stone-900">
          <Compass className="h-5 w-5 text-[#8C3A2A]" />
          Compass
        </div>
        <button
          onClick={() => go("app")}
          data-testid="landing-open-compass"
          className="text-sm font-mono-panel uppercase tracking-[0.18em] text-stone-500 hover:text-stone-900 transition-colors"
        >
          Open Compass
        </button>
      </header>

      {/* Hero */}
      <main className="flex-1 flex flex-col justify-center px-8 md:px-16 lg:px-24">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 py-24 md:py-32">
          <div className="lg:col-span-9 xl:col-span-8">
            <motion.span
              {...rise(0)}
              className="font-mono-panel text-xs md:text-sm tracking-[0.2em] uppercase text-[#8C3A2A] mb-7 block"
              data-testid="landing-eyebrow"
            >
              The problem with “help”
            </motion.span>

            <motion.h1
              {...rise(0.08)}
              className="font-serif-display text-5xl sm:text-6xl md:text-7xl tracking-tight leading-[1.02] text-stone-900 max-w-4xl"
              data-testid="landing-headline"
            >
              Writing is thinking.
              <br />
              <span className="text-[#8C3A2A]">Don’t let a machine do it for them.</span>
            </motion.h1>

            <motion.p
              {...rise(0.16)}
              className="text-lg md:text-xl text-stone-700 leading-relaxed mt-9 max-w-2xl"
              data-testid="landing-subcopy"
            >
              Most tools write the essay for your students. Compass does the
              opposite. It reads what a student is really trying to say, then asks
              the one question that makes them work it out themselves. It never
              writes a word for them.
            </motion.p>

            {/* Primary action */}
            <motion.div {...rise(0.24)} className="mt-12 flex flex-col items-start">
              <div className="flex flex-wrap items-center gap-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                  onClick={() => go("preview")}
                  data-testid="landing-try-preview"
                  className="group inline-flex items-center gap-2 bg-[#8C3A2A] text-white px-8 py-4 rounded-sm font-medium tracking-wide hover:bg-[#6B2C20] transition-colors focus:ring-2 focus:ring-[#8C3A2A] focus:outline-none"
                >
                  Try the Preview
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </motion.button>
                <button
                  onClick={() => go("represent")}
                  data-testid="landing-understand-assignment"
                  className="group inline-flex items-center gap-2 rounded-sm border border-stone-300 px-6 py-4 font-medium tracking-wide text-stone-700 transition-colors hover:border-[#8C3A2A] hover:text-[#8C3A2A] focus:outline-none focus:ring-2 focus:ring-[#8C3A2A]"
                >
                  Understand an assignment
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </button>
              </div>
              <span className="font-mono-panel text-xs text-stone-500 mt-4 tracking-wide">
                A 3-minute, in-character experience. No sign-up. You’ll be the writer.
              </span>
            </motion.div>
          </div>
        </div>
      </main>

      <footer className="px-8 md:px-16 lg:px-24 py-8 border-t border-stone-200">
        <p className="font-mono-panel text-[11px] uppercase tracking-[0.18em] text-stone-400">
          Compass · a developmental writing studio
        </p>
      </footer>
    </div>
  );
}
