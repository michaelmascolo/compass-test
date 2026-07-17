import { motion, AnimatePresence } from "framer-motion";
import { Terminal, X } from "lucide-react";

const Field = ({ label, children }) => (
  <div className="border-t border-stone-800 pt-3 mt-3 first:border-t-0 first:pt-0 first:mt-0">
    <div className="text-[10px] uppercase tracking-[0.2em] text-amber-500 mb-1.5">
      {label}
    </div>
    <div className="text-stone-300 leading-relaxed text-[13px]">{children}</div>
  </div>
);

const List = ({ items }) => {
  if (!items || items.length === 0)
    return <span className="text-stone-600">—</span>;
  return (
    <ul className="space-y-1.5">
      {items.map((it, i) => (
        <li key={i} className="flex gap-2">
          <span className="text-stone-600 select-none">›</span>
          <span>{it}</span>
        </li>
      ))}
    </ul>
  );
};

const Text = ({ value }) =>
  value ? <span>{value}</span> : <span className="text-stone-600">—</span>;

export default function DevelopmentPanel({ open, onClose, state, purpose }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-stone-950/30"
          />
          <motion.aside
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            data-testid="development-panel"
            className="fixed right-0 top-0 z-50 h-full w-full max-w-md bg-stone-900 border-l border-stone-800 flex flex-col font-mono-panel"
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-stone-800 shrink-0">
              <div className="flex items-center gap-2 text-stone-200">
                <Terminal className="h-4 w-4 text-amber-500" />
                <span className="text-xs uppercase tracking-[0.2em]">
                  Development Panel
                </span>
              </div>
              <button
                onClick={onClose}
                data-testid="close-dev-panel-button"
                className="text-stone-500 hover:text-stone-200 transition-colors"
                aria-label="Close development panel"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="px-5 py-3 border-b border-stone-800 shrink-0">
              <p className="text-[10px] text-stone-500 leading-relaxed">
                Testing only — the coach's evolving internal theory. Updated
                after every interaction.
              </p>
            </div>

            <div className="flex-1 overflow-y-auto custom-scroll px-5 py-5">
              <Field label="Current Pedagogical Purpose">
                <Text value={state?.current_pedagogical_purpose || purpose} />
              </Field>
              <Field label="Governing Purpose">
                <Text value={state?.governing_purpose} />
              </Field>
              <Field label="Developmental Theory · Organization Relative to Purpose">
                <Text value={state?.organization_relative_to_purpose} />
              </Field>
              <Field label="Direct Evidence">
                <List items={state?.direct_evidence} />
              </Field>
              <Field label="Primary Developmental Tension">
                <span className="text-amber-300">
                  <Text value={state?.primary_developmental_tension} />
                </span>
              </Field>
              <Field label="Alternative Interpretations">
                <List items={state?.alternative_interpretations} />
              </Field>
              <Field label="Selected Scaffold">
                <Text value={state?.selected_scaffold} />
              </Field>
              <Field label="Why That Scaffold">
                <Text value={state?.selection_basis} />
              </Field>
              <Field label="Candidate Scaffolds Considered">
                <List items={state?.candidate_scaffolds} />
              </Field>
              <Field label="Developmental Movement Detected">
                <Text value={state?.developmental_movement} />
              </Field>
              <Field label="Current Uncertainties">
                <List items={state?.uncertainties} />
              </Field>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
