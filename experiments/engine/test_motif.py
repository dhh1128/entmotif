#!/usr/bin/env python3
"""entmotif engine tests (zero-dep, assert-based). Run: python3 test_motif.py

Pins the SACRED invariants (determinism, avalanche) and the round-4 (v0.7)
fixes: bass chord-quality, lead never over-silent, final cadence resolves,
dynamics emitted. Exits nonzero on any failure.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motif                                                    # noqa: E402

DIV = motif.DIV
CORPUS = [ln.strip() for ln in open(os.path.join(HERE, "..", "teaching", "corpus.txt"))
          if ln.strip() and not ln.startswith("#")]

fails = []
def check(cond, msg):
    if not cond:
        fails.append(msg)


def bar_chord_pcs(m, bar):
    s = m["bar_chords"][bar]
    return [p % 12 for p in motif.cpcs(s, m["mode"], m["key"])]


# --- SACRED: determinism (same input -> identical notes, meta, MIDI bytes) ---
for v in CORPUS:
    n1, m1 = motif.generate(v)
    n2, m2 = motif.generate(v)
    check(n1 == n2 and m1 == m2, "determinism(notes/meta): %s" % v)
    motif.write_midi(n1, m1["tempo"], m1["lead_prog"], m1["ans_prog"], "/tmp/_a.mid")
    motif.write_midi(n2, m2["tempo"], m2["lead_prog"], m2["ans_prog"], "/tmp/_b.mid")
    check(open("/tmp/_a.mid", "rb").read() == open("/tmp/_b.mid", "rb").read(),
          "determinism(midi bytes): %s" % v)

# --- SACRED: avalanche (one-char change -> different motif) ---
na, _ = motif.generate("did:example:alice")
nb, _ = motif.generate("did:example:alife")
check(na != nb, "avalanche: alice vs alife identical")

# --- round-4: bass notes must be chord tones of the active chord ---
for v in CORPUS:
    notes, m = motif.generate(v)
    for (chan, pitch, vel, start, dur) in notes:
        if chan == 2:
            bar = start // (4 * DIV)
            if bar < m["bars"]:
                pcs = bar_chord_pcs(m, bar)
                check(pitch % 12 in pcs,
                      "bass non-chord-tone: %s bar%d pc%d not in %s" % (v, bar, pitch % 12, pcs))

# --- round-4: final cadence resolves (last melodic note in the tonic triad) ---
for v in CORPUS:
    notes, m = motif.generate(v)
    mel = [n for n in notes if n[0] in (0, 3)]
    last = max(mel, key=lambda n: n[3])
    tonic = [p % 12 for p in motif.cpcs("I" if m["mode"] == "major" else "i", m["mode"], m["key"])]
    check(last[1] % 12 in tonic,
          "final unresolved: %s ends on pc%d (tonic triad %s)" % (v, last[1] % 12, tonic))

# --- round-4: lead (chan 0) never silent for a whole 2-bar unit (except groove intro) ---
for v in CORPUS:
    notes, m = motif.generate(v)
    nU = m["bars"] // 2
    for u in range(nU):
        lo, hi = u * 2 * 4 * DIV, (u + 1) * 2 * 4 * DIV
        if m["arr"] == "groove_first" and u == 0:
            continue
        has = any(n[0] == 0 and lo <= n[3] < hi for n in notes)
        check(has, "lead silent in unit %d: %s (arr=%s)" % (u, v, m["arr"]))

# --- round-4: dynamics emitted in ABC ---
for v in CORPUS:
    notes, m = motif.generate(v)
    check("!" in motif.abc_export(v, notes, m), "no dynamics in ABC: %s" % v)

print("CORPUS=%d   FAILURES=%d" % (len(CORPUS), len(fails)))
for f in fails[:50]:
    print("  -", f)
sys.exit(1 if fails else 0)
