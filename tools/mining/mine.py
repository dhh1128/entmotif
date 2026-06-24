#!/usr/bin/env python3
"""entmotif corpus miner — extract conditional distributions from a vendored/fetched corpus.

Re-runnable and idempotent: same corpus in → byte-identical feature JSON out. The
fingerprint-driven generator later samples a CDF point from these distributions; mining
itself never touches ``src/entmotif/``.

    python3 tools/mining/mine.py --dataset thesession --feature meter
    python3 tools/mining/mine.py --dataset thesession --feature all
    python3 tools/mining/mine.py --list
    python3 tools/mining/mine.py --dataset emopia --feature emotion --limit 200

Output: data/features/<dataset>.<feature>.json  (small, committed).

To ADD a feature, see tools/mining/features/__init__.py.
To ADD a dataset, see tools/mining/datasets.py.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # allow `import ir`, `import datasets`, `import features`

import datasets  # noqa: E402
from features import FEATURES  # noqa: E402

OUT_DIR = os.path.join(datasets.REPO, "data", "features")


def _provenance(dataset, n_tunes, limit):
    return {
        "dataset": dataset,
        "n_tunes_loaded": n_tunes,
        "limit": limit,
        "tool": "tools/mining/mine.py",
        "note": "Derived aggregate statistics — not a redistribution of the source corpus.",
    }


def run_feature(dataset, feature, tunes, limit):
    mod = FEATURES[feature]
    result = mod.run(tunes)
    payload = {
        "feature": feature,
        "description": mod.DESC,
        "requires": list(mod.REQUIRES),
        "provenance": _provenance(dataset, len(tunes), limit),
        "distribution": result,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "%s.%s.json" % (dataset, feature))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", help="corpus name (see --list)")
    ap.add_argument("--feature", help="feature name, or 'all'")
    ap.add_argument("--limit", type=int, default=None, help="cap tunes loaded (for sampling)")
    ap.add_argument("--list", action="store_true", help="list datasets + features and exit")
    args = ap.parse_args(argv)

    if args.list or not (args.dataset and args.feature):
        print("datasets:", ", ".join(datasets.DATASETS))
        print("features:")
        for name, mod in FEATURES.items():
            print("  %-15s %s" % (name, mod.DESC))
        return 0

    feats = list(FEATURES) if args.feature == "all" else [args.feature]
    for f in feats:
        if f not in FEATURES:
            raise SystemExit("unknown feature %r; see --list" % f)

    tunes = list(datasets.load(args.dataset, limit=args.limit))
    print("loaded %d tunes from %s" % (len(tunes), args.dataset))
    for f in feats:
        out = run_feature(args.dataset, f, tunes, args.limit)
        print("  wrote", os.path.relpath(out, datasets.REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
