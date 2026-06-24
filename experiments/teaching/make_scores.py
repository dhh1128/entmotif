#!/usr/bin/env python3
"""Generate the ABC score bundle for the frozen corpus, for teacher grading.

Usage: python3 make_scores.py <engine-version-label>   (default: dev)
Writes scores-<label>.md next to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import motif                                                   # noqa: E402

label = sys.argv[1] if len(sys.argv) > 1 else "dev"
corpus = [ln.strip() for ln in open(os.path.join(HERE, "corpus.txt"))
          if ln.strip() and not ln.startswith("#")]

out = ["# entmotif scores — engine %s" % label,
       "",
       "Fixed corpus; ABC lead-sheets (melody + chord symbols) for grading.",
       "L:1/16, K:C with explicit accidentals; the C: header gives key/mode/"
       "tempo/form. Each score is one input value rendered by the engine.", ""]
for i, v in enumerate(corpus, 1):
    notes, m = motif.generate(v)
    out.append("## Score %d  —  `%s`" % (i, v))
    out.append("(%s/%s, %s %s, %dbpm, %s, %d bars, lead=%s, leap=%s, arr=%s, fat=%d)"
               % (m["style"], m.get("emotion", "-"), motif.KEY_NAMES[m["key"]], m["mode"],
                  m["tempo"], m["form"], m["bars"], m["lead"], m["leap"], m["arr"], m["fat"]))
    out.append("```abc\n%s```\n" % motif.abc_export(v, notes, m))
path = os.path.join(HERE, "scores-%s.md" % label)
open(path, "w").write("\n".join(out))
print("wrote %s (%d scores)" % (path, len(corpus)))
