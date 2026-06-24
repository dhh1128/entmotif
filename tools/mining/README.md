# entmotif corpus mining

A small, **low-dep** (numpy/scipy only — pure-Python parsers, no `music21`/`mido`),
**re-runnable** pipeline that mines human-authored music corpora into **conditional
probability distributions** for entmotif's decision DAG (`this.i:d2k9m4p1`,
`this.i:v8k2m1p0`). It does **not** touch `src/entmotif/` and does **not** train a
neural model — every output is a small histogram/percentile table we can sample
deterministically later (the entropy fingerprint picks a CDF point, per
`this.i:7c4m1k0p`).

## Run it

```bash
./data/fetch.sh thesession            # download a corpus into data/raw/ (gitignored)
./data/fetch.sh emopia                # ~5.5 MB EMOPIA MIDI (CC BY 4.0)

python3 tools/mining/mine.py --list                                   # datasets + features
python3 tools/mining/mine.py --dataset thesession --feature meter     # one feature
python3 tools/mining/mine.py --dataset thesession --feature all       # every feature
python3 tools/mining/mine.py --dataset emopia --feature emotion --limit 200

python3 tools/mining/test_mining.py   # offline self-test (no corpus/network needed)
```

Output lands in `data/features/<dataset>.<feature>.json` — small and **committed**
(derived aggregate stats are not a redistribution of the source corpus). Runs are
**idempotent**: same corpus in → byte-identical JSON out (sorted keys, fixed rounding).

## Layout

```
tools/mining/
  ir.py            normalized intermediate representation (Tune / Note); beats + MIDI pitch
  parsers/abc.py   tolerant ABC → IR (TheSession, Nottingham). Applies key signatures.
  parsers/midi.py  minimal Standard-MIDI-File reader → IR (EMOPIA, VGMIDI)
  datasets.py      per-corpus loaders → stream of Tune; locates data/raw or data/vendor
  featlib.py       histogram / conditional / percentile helpers
  features/        one module per feature (see registry in features/__init__.py)
  mine.py          CLI entry point
  test_mining.py   offline regression test
```

## How to ADD A FEATURE

1. Create `tools/mining/features/<name>.py` exposing four names:
   ```python
   NAME = "voicing_density"
   DESC = "P(simultaneous-note count) — texture/voicing density"
   REQUIRES = ("notes",)                 # Tune fields the extractor reads
   def run(tunes):                       # tunes: list[ir.Tune]
       ...                               # return a small, JSON-serializable dict of
       return {...}                      # normalized histograms / percentiles
   ```
   Use `featlib.histogram / conditional / percentiles` so outputs stay small and
   sample-able. For a **conditional** distribution, key the output by the conditioning
   context and include the per-context sample size (a `*_support` map) so thin rows
   carry a sample-size caveat (`this.i` evidence-grounding discipline).
2. Register it: add the module to `_MODULES` in `features/__init__.py`.
3. `python3 tools/mining/mine.py --dataset <d> --feature <name>` picks it up; add a
   fixture assertion to `test_mining.py`.

## How to ADD A DATASET

1. Write `load_<name>(root) -> Iterable[ir.Tune]` in `datasets.py` (reuse a parser in
   `parsers/`, or add one). Normalize everything into beats + MIDI pitch in the IR.
2. Register it in the `DATASETS` dict.
3. Add a `fetch_<name>()` to `data/fetch.sh` that downloads into `data/raw/<name>/` and
   records URL + sha256. **Honor the license** — see `data/README.md`. Commit only
   derived stats unless the corpus is small AND cleanly permissive.

## Mapping mined vectors onto the engine

Mining is intentionally **upstream of and independent from** the engine's vocabulary.
The translation (e.g. EMOPIA register percentiles → `PitchRange(lo, center, hi)`;
emotion→mode probabilities → the `mode_w` knob; meter histogram → the meter-expansion
track) is done by hand and reviewed — see `docs/corpus-mining-findings.md`. Keeping the
mapping out of code keeps determinism in the engine and auditability in the data.
