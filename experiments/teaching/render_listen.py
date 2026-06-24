#!/usr/bin/env python3
"""Render the frozen corpus to MIDI + WAV for a maintainer listening pass.

Usage: python3 render_listen.py <label> <out-dir>
Writes <out-dir>/NN-<style>-<emotion>.mid and .wav for each corpus input, plus an
index.txt naming each track. Audio is regenerable + perceptual, NOT the source of
truth (this.i:3k7a92f0) — the .mid is canonical.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import motif                                                   # noqa: E402

SF2 = os.path.join(HERE, "..", "soundfont", "sf", "GeneralUser-GS.sf2")
label = sys.argv[1] if len(sys.argv) > 1 else "dev"
outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
corpus = [ln.strip() for ln in open(os.path.join(HERE, "corpus.txt"))
          if ln.strip() and not ln.startswith("#")]

index = []
for i, v in enumerate(corpus, 1):
    notes, m = motif.generate(v)
    stem = "%02d-%s-%s-%s" % (i, m["style"], m.get("emotion", "x"), m["lead"].replace(" ", ""))
    mid = os.path.join(outdir, stem + ".mid")
    wav = os.path.join(outdir, stem + ".wav")
    motif.write_midi(notes, m, mid)
    subprocess.run(["fluidsynth", "-ni", "-F", wav, "-r", "44100", SF2, mid],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    line = "%2d. %-13s %-10s %3dbpm %-5s lead=%-13s  `%s`" % (
        i, m["style"], m.get("emotion", "x"), m["tempo"], m["mode"], m["lead"], v[:40])
    index.append(line)
    print("rendered", stem)

open(os.path.join(outdir, "index.txt"), "w").write(
    "entmotif %s — listening pass\n\n" % label + "\n".join(index) + "\n")
print("\nINDEX:\n" + "\n".join(index))
