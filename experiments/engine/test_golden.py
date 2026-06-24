#!/usr/bin/env python3
"""Golden-output snapshot guard for the entmotif engine (zero-dep).

Pins the EXACT current output (ABC text + MIDI bytes) for the frozen corpus, so the
upcoming refactor (docs/refactor-plan.md) is provably behavior-preserving: any step
that changes a single note fails here and names the input that drifted.

  python3 test_golden.py            # compare current output to the committed golden/
  python3 test_golden.py --update   # (re)write golden/ fixtures from current output

Golden fixtures (committed): golden/<idx>.abc  (full ABC, human-diffable)
                             golden/midi.tsv   (idx \\t input \\t sha256(midi bytes))
Run after EVERY refactor step. A drift here is a regression unless explicitly intended
(if intended, re-run --update and review the diff before committing).
"""
import hashlib
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motif                                                    # noqa: E402

GOLD = os.path.join(HERE, "golden")
CORPUS = [ln.strip() for ln in open(os.path.join(HERE, "..", "teaching", "corpus.txt"))
          if ln.strip() and not ln.startswith("#")]
UPDATE = "--update" in sys.argv


def current(value):
    notes, m = motif.generate(value)
    abc = motif.abc_export(value, notes, m)
    tmp = os.path.join(tempfile.gettempdir(), "_golden.mid")
    motif.write_midi(notes, m["tempo"], m["lead_prog"], m["ans_prog"], tmp)
    midi_sha = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
    return abc, midi_sha


if UPDATE:
    os.makedirs(GOLD, exist_ok=True)
    rows = []
    for i, v in enumerate(CORPUS, 1):
        abc, midi_sha = current(v)
        open(os.path.join(GOLD, "%02d.abc" % i), "w").write(abc)
        rows.append("%d\t%s\t%s" % (i, v, midi_sha))
    open(os.path.join(GOLD, "midi.tsv"), "w").write("\n".join(rows) + "\n")
    print("wrote golden/ fixtures for %d corpus inputs" % len(CORPUS))
    sys.exit(0)

if not os.path.isdir(GOLD):
    print("no golden/ fixtures — run: python3 test_golden.py --update")
    sys.exit(1)

gold_midi = {}
for ln in open(os.path.join(GOLD, "midi.tsv")):
    idx, v, sha = ln.rstrip("\n").split("\t")
    gold_midi[int(idx)] = (v, sha)

fails = []
for i, v in enumerate(CORPUS, 1):
    abc, midi_sha = current(v)
    gpath = os.path.join(GOLD, "%02d.abc" % i)
    if not os.path.exists(gpath):
        fails.append("missing golden ABC for #%d (%s)" % (i, v))
    elif open(gpath).read() != abc:
        fails.append("ABC drift: #%d (%s)" % (i, v))
    gv, gsha = gold_midi.get(i, (None, None))
    if gv != v:
        fails.append("corpus changed at #%d: golden=%r current=%r" % (i, gv, v))
    elif gsha != midi_sha:
        fails.append("MIDI drift: #%d (%s)" % (i, v))

print("CORPUS=%d   GOLDEN FAILURES=%d" % (len(CORPUS), len(fails)))
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
