# Canon Calibration — grounding the teaching loop in real greatness

The teaching loop (`prompts/teaching/`) currently grades the engine on the
faculty's *general taste*. **Canon Calibration** grounds it in evidence, two ways:

1. **Grade the greats.** Assemble a cross-genre canon of ~50 acknowledged-great,
   earworm-defensible themes, transcribe each theme's identifiable phrase to ABC,
   and run them through *our faculty on our rubric*. This:
   - **validates the rubric/teachers** — if real masterpieces don't score A's, our
     rubric is mis-calibrated (or grading-from-notation misses what makes them
     great — itself a finding);
   - **distills what greatness looks like** on our axes → sharper rubric criteria
     and better engine priors;
   - gives a **gold-standard reference score** the engine is chasing.
2. **Read the research.** Find + verify the academic literature on melodic
   memorability / earworms, and fold confirmed findings into the rubric + priors.

## Phases & on-disk outputs (everything is stored, nothing lives only in chat)

| Phase | Prompt | Output on disk |
|---|---|---|
| 1. Build the canon list | `build-canon.md` | `docs/canon.md` (list + sources) |
| 1b. Transcribe to ABC | (in `build-canon.md`, phase 2) | `experiments/teaching/canon/abc/<id>.abc` |
| 2. Research memorability | `research-memorability.md` | `docs/memorability-research.md` (annotated bib + synthesis) |
| 3. Grade the greats | run the `prompts/teaching/` faculty over the canon ABC | `docs/engine-log.md` calibration entry + rubric/prior updates |

Verification discipline (same as `docs/references.md`): every source/claim records
whether it was independently verified; never cite an unverified source as verified.
Canon entries that depend on lyrics/timbre/performance (not the melody) are flagged,
because ABC can't carry those — discovering which greatness is notation-visible is
part of the point.
