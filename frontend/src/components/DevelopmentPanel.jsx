import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, X, Pencil, Save, RotateCcw } from "lucide-react";

const SectionLabel = ({ children }) => (
  <div className="text-[10px] uppercase tracking-[0.2em] text-amber-500 mb-1.5">
    {children}
  </div>
);

const Block = ({ label, children }) => (
  <div className="border-t border-stone-800 pt-3 mt-3 first:border-t-0 first:pt-0 first:mt-0">
    <SectionLabel>{label}</SectionLabel>
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

function TelosEditor({ session, onSave, saving }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    assignment: session.assignment,
    pedagogical_purpose: session.pedagogical_purpose,
    current_writing_task: session.current_writing_task,
  });

  useEffect(() => {
    setForm({
      assignment: session.assignment,
      pedagogical_purpose: session.pedagogical_purpose,
      current_writing_task: session.current_writing_task,
    });
  }, [session.assignment, session.pedagogical_purpose, session.current_writing_task]);

  const field = (key, label) => (
    <div>
      <SectionLabel>{label}</SectionLabel>
      <textarea
        data-testid={`telos-edit-${key}`}
        value={form[key]}
        onChange={(e) => setForm({ ...form, [key]: e.target.value })}
        rows={2}
        className="w-full bg-stone-950 border border-stone-700 rounded-sm p-2 text-[12px] text-stone-200 outline-none focus:border-amber-500 transition-colors resize-none"
      />
    </div>
  );

  return (
    <div className="border-b border-stone-800">
      <button
        data-testid="toggle-telos-editor"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-5 py-2.5 text-stone-400 hover:text-stone-100 transition-colors"
      >
        <span className="flex items-center gap-2 text-[11px] uppercase tracking-[0.18em]">
          <Pencil className="h-3 w-3" /> Teacher · revise telos
        </span>
        <RotateCcw className={`h-3 w-3 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-4 space-y-3">
              {field("assignment", "Assignment")}
              {field("pedagogical_purpose", "Pedagogical Purpose")}
              {field("current_writing_task", "Current Writing Task")}
              <button
                data-testid="save-telos-button"
                onClick={() => onSave(form)}
                disabled={saving}
                className="inline-flex items-center gap-1.5 bg-amber-500 text-stone-900 px-3 py-1.5 rounded-sm text-[11px] uppercase tracking-[0.15em] font-medium hover:bg-amber-400 transition-colors disabled:opacity-40"
              >
                <Save className="h-3 w-3" />
                {saving ? "Saving…" : "Save telos"}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function DevelopmentPanel({
  open,
  onClose,
  session,
  onEditTelos,
  savingTelos,
}) {
  if (!session) return null;
  const theory = session.theory || {};
  const telos = session.telos || {};
  const interactions = session.interactions || [];
  const last = interactions[interactions.length - 1];

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
                  Developmental Guide Engine
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

            <TelosEditor
              session={session}
              onSave={onEditTelos}
              saving={savingTelos}
            />

            <div className="px-5 py-2.5 border-b border-stone-800 shrink-0">
              <p className="text-[10px] text-stone-500 leading-relaxed">
                Testing / teacher review — provisional working theory of the
                developing system. Revised (not appended) each turn.
                {session.theory_history?.length
                  ? ` v${session.theory_history.length + 1}`
                  : " v1"}
              </p>
            </div>

            <div className="flex-1 overflow-y-auto custom-scroll px-5 py-5">
              <Block label="Current Telos">
                <Text value={theory.current_telos || telos.governing_pedagogical_purpose} />
              </Block>
              <Block label="Communicative Purpose">
                <div className="space-y-1.5" data-testid="communicative-purpose-block">
                  <div>
                    <span className="text-stone-500">primary:</span>{" "}
                    <span className="text-amber-300">
                      <Text value={theory.communicative_purpose?.primary} />
                    </span>
                  </div>
                  <div>
                    <span className="text-stone-500">secondary:</span>{" "}
                    <List items={theory.communicative_purpose?.secondary} />
                  </div>
                  <div>
                    <span className="text-stone-500">inferred from:</span>{" "}
                    <Text value={theory.communicative_purpose?.inferred_from} />
                  </div>
                  {theory.communicative_purpose?.uncertainty ? (
                    <div>
                      <span className="text-stone-500">uncertainty:</span>{" "}
                      <Text value={theory.communicative_purpose?.uncertainty} />
                    </div>
                  ) : null}
                </div>
              </Block>
              <Block label="Scaffolding Controller (M11)">
                <div className="space-y-1.5" data-testid="scaffolding-control-block">
                  <div>
                    <span className="text-stone-500">unit:</span>{" "}
                    <Text value={theory.scaffolding_control?.current_unit} />
                  </div>
                  <div>
                    <span className="text-stone-500">diagnosed opportunities:</span>{" "}
                    <List items={theory.scaffolding_control?.diagnosed_opportunities} />
                  </div>
                  <div>
                    <span className="text-stone-500">primary target:</span>{" "}
                    <span className="text-amber-300">
                      <Text value={theory.scaffolding_control?.primary_target} />
                    </span>
                  </div>
                  <div>
                    <span className="text-stone-500">why (priority):</span>{" "}
                    <Text value={theory.scaffolding_control?.prioritization_rationale} />
                  </div>
                  <div>
                    <span className="text-stone-500">mode:</span>{" "}
                    <span className="text-emerald-300">
                      <Text value={theory.scaffolding_control?.instructional_mode} />
                    </span>
                  </div>
                  <div>
                    <span className="text-stone-500">postponed:</span>{" "}
                    <List items={theory.scaffolding_control?.postponed} />
                  </div>
                  <div>
                    <span className="text-stone-500">cycle status:</span>{" "}
                    <span className="text-sky-300">
                      <Text value={theory.scaffolding_control?.cycle_status} />
                    </span>
                  </div>
                  {theory.scaffolding_control?.stopping_reason ? (
                    <div>
                      <span className="text-stone-500">stopping reason:</span>{" "}
                      <Text value={theory.scaffolding_control?.stopping_reason} />
                    </div>
                  ) : null}
                  {theory.scaffolding_control?.future_opportunity ? (
                    <div>
                      <span className="text-stone-500">future opportunity:</span>{" "}
                      <Text value={theory.scaffolding_control?.future_opportunity} />
                    </div>
                  ) : null}
                </div>
              </Block>
              {theory.reader_construction?.applies ? (
                <Block label="Reader Construction (M12)">
                  <div className="space-y-1.5" data-testid="reader-construction-block">
                    <div>
                      <span className="text-stone-500">reader understands:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.reader_construction?.reader_understanding} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">likely questions:</span>{" "}
                      <List items={theory.reader_construction?.likely_reader_questions} />
                    </div>
                    <div>
                      <span className="text-stone-500">assumed knowledge:</span>{" "}
                      <Text value={theory.reader_construction?.assumed_knowledge} />
                    </div>
                    <div>
                      <span className="text-stone-500">clarification needed:</span>{" "}
                      <Text value={theory.reader_construction?.clarification_needed} />
                    </div>
                    <div>
                      <span className="text-stone-500">elaboration needed:</span>{" "}
                      <Text value={theory.reader_construction?.elaboration_needed} />
                    </div>
                    <div>
                      <span className="text-stone-500">precision risk:</span>{" "}
                      <Text value={theory.reader_construction?.precision_risk} />
                    </div>
                    <div>
                      <span className="text-stone-500">next reader need:</span>{" "}
                      <span className="text-sky-300">
                        <Text value={theory.reader_construction?.next_reader_need} />
                      </span>
                    </div>
                  </div>
                </Block>
              ) : null}
              {theory.revision_development?.applies ? (
                <Block label="Revision as Development (M13)">
                  <div className="space-y-1.5" data-testid="revision-development-block">
                    <div>
                      <span className="text-stone-500">development detected:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.revision_development?.development_detected} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">primary growth:</span>{" "}
                      <Text value={theory.revision_development?.primary_growth} />
                    </div>
                    <div>
                      <span className="text-stone-500">communication change:</span>{" "}
                      <Text value={theory.revision_development?.communication_change} />
                    </div>
                    <div>
                      <span className="text-stone-500">reader change:</span>{" "}
                      <Text value={theory.revision_development?.reader_change} />
                    </div>
                    <div>
                      <span className="text-stone-500">remaining opportunity:</span>{" "}
                      <Text value={theory.revision_development?.remaining_opportunity} />
                    </div>
                    <div>
                      <span className="text-stone-500">transfer message:</span>{" "}
                      <span className="text-emerald-300">
                        <Text value={theory.revision_development?.transfer_message} />
                      </span>
                    </div>
                  </div>
                </Block>
              ) : null}
                <Block label="Paragraph Function (M7)">
                  <div className="space-y-1.5" data-testid="paragraph-function-block">
                    <div>
                      <span className="text-stone-500">purpose:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.paragraph_function?.purpose} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">contribution to whole:</span>{" "}
                      <Text value={theory.paragraph_function?.contribution_to_whole} />
                    </div>
                    <div>
                      <span className="text-stone-500">coherence:</span>{" "}
                      <Text value={theory.paragraph_function?.coherence} />
                    </div>
                    <div>
                      <span className="text-stone-500">development:</span>{" "}
                      <Text value={theory.paragraph_function?.development} />
                    </div>
                    <div>
                      <span className="text-stone-500">placement:</span>{" "}
                      <Text value={theory.paragraph_function?.placement} />
                    </div>
                  </div>
                </Block>
              ) : null}
              {theory.evidence_function?.applies ? (
                <Block label="Evidence Function (M8)">
                  <div className="space-y-1.5" data-testid="evidence-function-block">
                    <div>
                      <span className="text-stone-500">forms:</span>{" "}
                      <List items={theory.evidence_function?.forms} />
                    </div>
                    <div>
                      <span className="text-stone-500">function:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.evidence_function?.function} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">interpretation gap:</span>{" "}
                      <Text value={theory.evidence_function?.interpretation_gap} />
                    </div>
                    <div>
                      <span className="text-stone-500">quality (functional):</span>{" "}
                      <Text value={theory.evidence_function?.quality} />
                    </div>
                  </div>
                </Block>
              ) : null}
              {theory.coherence_function?.applies ? (
                <Block label="Transitions & Coherence (M9)">
                  <div className="space-y-1.5" data-testid="coherence-function-block">
                    <div>
                      <span className="text-stone-500">intended relationship:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.coherence_function?.intended_relationship} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">level:</span>{" "}
                      <Text value={theory.coherence_function?.level} />
                    </div>
                    <div>
                      <span className="text-stone-500">resources in use:</span>{" "}
                      <List items={theory.coherence_function?.resources_in_use} />
                    </div>
                    <div>
                      <span className="text-stone-500">reader can follow:</span>{" "}
                      <Text value={theory.coherence_function?.reader_can_follow} />
                    </div>
                  </div>
                </Block>
              ) : null}
              {theory.conclusion_function?.applies ? (
                <Block label="Conclusion / Completion (M10)">
                  <div className="space-y-1.5" data-testid="conclusion-function-block">
                    <div>
                      <span className="text-stone-500">functions in play:</span>{" "}
                      <List items={theory.conclusion_function?.functions_in_play} />
                    </div>
                    <div>
                      <span className="text-stone-500">completes purpose:</span>{" "}
                      <span className="text-amber-300">
                        <Text value={theory.conclusion_function?.completes_purpose} />
                      </span>
                    </div>
                    <div>
                      <span className="text-stone-500">relationship to opening:</span>{" "}
                      <Text value={theory.conclusion_function?.relationship_to_opening} />
                    </div>
                    <div>
                      <span className="text-stone-500">final understanding:</span>{" "}
                      <Text value={theory.conclusion_function?.final_understanding} />
                    </div>
                  </div>
                </Block>
              ) : null}
              <Block label="Current Organization (relative to telos)">
                <Text value={theory.current_organization} />
              </Block>
              <Block label="Observed Developmental Movement">
                <div className="space-y-2">
                  <div>
                    <span className="text-stone-500">differentiation:</span>{" "}
                    <List items={theory.observed_differentiations} />
                  </div>
                  <div>
                    <span className="text-stone-500">integration:</span>{" "}
                    <List items={theory.observed_integrations} />
                  </div>
                  <div>
                    <span className="text-stone-500">coordination:</span>{" "}
                    <List items={theory.observed_coordinations} />
                  </div>
                  <div>
                    <span className="text-stone-500">intentional control:</span>{" "}
                    <Text value={theory.emerging_intentional_control} />
                  </div>
                </div>
              </Block>
              <Block label="Currently Relevant Canonical Domains">
                <List items={theory.currently_relevant_domains} />
              </Block>
              <Block label="Active Tension(s)">
                <span className="text-amber-300">
                  <List items={theory.unresolved_tensions} />
                </span>
              </Block>
              <Block label="Cultural Resources (in use / potential)">
                <div className="space-y-1.5">
                  <div>
                    <span className="text-stone-500">in use:</span>{" "}
                    <List items={theory.cultural_resources_in_use} />
                  </div>
                  <div>
                    <span className="text-stone-500">potential:</span>{" "}
                    <List items={theory.potential_cultural_resources} />
                  </div>
                </div>
              </Block>
              <Block label="Evidence — Supporting">
                <List items={theory.supporting_evidence} />
              </Block>
              <Block label="Evidence — Complicating / Contradicting">
                <List items={theory.complicating_evidence} />
              </Block>
              <Block label="Alternative Interpretations (preserved)">
                <List items={theory.alternative_interpretations} />
              </Block>
              <Block label="Current Uncertainty">
                <List items={theory.current_uncertainty} />
              </Block>
              <Block label="Possible Reorganizations">
                <List items={theory.possible_reorganizations} />
              </Block>

              <Block label="Candidate Invitations (internal)">
                {last?.candidate_invitations?.length ? (
                  <div className="space-y-3">
                    {last.candidate_invitations.map((c, i) => (
                      <div
                        key={i}
                        data-testid={`candidate-invitation-${i}`}
                        className="border border-stone-800 rounded-sm p-2.5 bg-stone-950/50"
                      >
                        <div className="text-stone-200">
                          {i + 1}. {c.invitation}
                        </div>
                        <div className="text-[11px] text-stone-500 mt-1">
                          addresses: {c.developmental_possibility || "—"}
                        </div>
                        <div className="text-[11px] text-stone-500">
                          could learn: {c.what_ai_could_learn || "—"}
                        </div>
                        <div className="text-[11px] text-stone-500">
                          risk: {c.uncertainty_or_risk || "—"}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <span className="text-stone-600">—</span>
                )}
              </Block>
              <Block label="Selected Invitation">
                <div className="text-amber-200" data-testid="selected-invitation">
                  <Text value={last?.selected_invitation?.invitation} />
                </div>
              </Block>
              <Block label="Developmental Instruction — Intervention">
                <div className="space-y-1.5" data-testid="intervention-block">
                  <div>
                    <span className="text-stone-500">type:</span>{" "}
                    <span className="text-amber-300">
                      <Text value={last?.intervention?.type} />
                    </span>
                  </div>
                  <div>
                    <span className="text-stone-500">cultural resource:</span>{" "}
                    <Text value={last?.intervention?.cultural_resource} />
                  </div>
                  <div>
                    <span className="text-stone-500">interpretation:</span>{" "}
                    <Text value={last?.intervention?.interpretation} />
                  </div>
                  <div>
                    <span className="text-stone-500">instruction:</span>{" "}
                    <Text value={last?.intervention?.instruction} />
                  </div>
                  <div>
                    <span className="text-stone-500">consolidation:</span>{" "}
                    <Text value={last?.intervention?.consolidation} />
                  </div>
                  <div>
                    <span className="text-stone-500">timing:</span>{" "}
                    <Text value={last?.intervention?.timing_rationale} />
                  </div>
                  <div>
                    <span className="text-stone-500">focus:</span>{" "}
                    <span className={last?.intervention?.focus === "content" ? "text-orange-300" : "text-emerald-300"}>
                      <Text value={last?.intervention?.focus} />
                    </span>
                  </div>
                  <div>
                    <span className="text-stone-500">writing-not-content check:</span>{" "}
                    <Text value={last?.intervention?.writing_not_content_check} />
                  </div>
                </div>
              </Block>
              <Block label="Rationale for Selection (coherence, not optimality)">
                <Text value={last?.selected_invitation?.selection_basis} />
              </Block>
              <Block label="Change From Previous Interaction">
                <Text value={theory.changes_since_previous} />
              </Block>
              <Block label="Observed Reorganization (this turn)">
                <Text value={last?.observed_reorganization} />
              </Block>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
