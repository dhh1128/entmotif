"""Dataset loaders: each yields a stream of normalized :class:`ir.Tune` records.

A loader locates its corpus under ``data/raw/<name>/`` (fetched, gitignored) or
``data/vendor/<name>/`` (small + permissive, committed), parses it with the right
parser, and normalizes into the IR. To ADD A DATASET: write a generator
``load_<name>(root) -> Iterable[Tune]`` and register it in ``DATASETS``.
"""
from __future__ import annotations

import glob
import json
import os
import re

from ir import Tune
from parsers.abc import parse_abc
from parsers.midi import parse_midi

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def data_dir(name):
    """Return the corpus directory: raw (fetched) preferred, else vendor (committed)."""
    for sub in ("raw", "vendor"):
        d = os.path.join(REPO, "data", sub, name)
        if os.path.isdir(d):
            return d
    return None


# --- TheSession (ABC + JSON metadata; CC0) -----------------------------------------
def load_thesession(root):
    path = os.path.join(root, "tunes.json")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        rows = json.load(fh)
    for r in rows:
        abc = r.get("abc")
        if not abc:
            continue
        # headers may be missing from the abc body; supply M:/K: from the metadata
        header = []
        if r.get("meter"):
            header.append("M:" + r["meter"])
        if r.get("mode"):
            tonic = r["mode"][0]
            header.append("K:" + tonic + _mode_suffix(r["mode"]))
        tune = parse_abc("\n".join(header) + "\nL:1/8\n" + abc,
                         source="thesession",
                         ident=str(r.get("setting_id") or r.get("tune_id") or ""))
        if not tune:
            continue
        if r.get("meter") and "/" in r["meter"]:
            num, den = r["meter"].split("/")
            tune.meter = (int(num), int(den))
        if r.get("mode"):
            tune.mode = _mode_name(r["mode"])
        tune.genre = r.get("type")
        yield tune


_MODE_WORDS = ("major", "minor", "dorian", "mixolydian", "phrygian", "lydian",
               "locrian", "ionian", "aeolian")


def _mode_name(mode_field):
    low = mode_field.lower()
    for w in _MODE_WORDS:
        if w in low:
            return {"ionian": "major", "aeolian": "minor"}.get(w, w)
    return None


def _mode_suffix(mode_field):
    name = _mode_name(mode_field) or "major"
    return {"major": "", "minor": "m", "dorian": "dor", "mixolydian": "mix",
            "phrygian": "phr", "lydian": "lyd", "locrian": "loc"}.get(name, "")


# --- Nottingham (raw multi-tune ABC files; public domain) --------------------------
def load_nottingham(root):
    for path in sorted(glob.glob(os.path.join(root, "**", "*.abc"), recursive=True)):
        genre = re.sub(r"\d+$", "", os.path.splitext(os.path.basename(path))[0]) or None
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for chunk in re.split(r"\n(?=X:)", text):
            if "K:" not in chunk:
                continue
            m = re.search(r"X:\s*(\d+)", chunk)
            tune = parse_abc(chunk, source="nottingham", ident=m.group(1) if m else "")
            if tune:
                tune.genre = genre
                yield tune


# --- EMOPIA / VGMIDI (emotion-labelled MIDI) ---------------------------------------
_QUAD = re.compile(r"Q([1-4])")


def load_midi_emotion(root, source):
    paths = glob.glob(os.path.join(root, "**", "*.mid"), recursive=True) + \
        glob.glob(os.path.join(root, "**", "*.midi"), recursive=True)
    for path in sorted(paths):
        base = os.path.basename(path)
        if "__MACOSX" in path or base.startswith("._"):   # AppleDouble fork junk in zips
            continue
        m = _QUAD.search(base)
        emotion = ("Q" + m.group(1)) if m else None
        try:
            with open(path, "rb") as fh:
                data = fh.read()
            tune = parse_midi(data, source=source, ident=os.path.basename(path),
                              emotion=emotion)
        except Exception:
            continue
        if tune:
            yield tune


def load_emopia(root):
    return load_midi_emotion(root, "emopia")


def load_vgmidi(root):
    return load_midi_emotion(root, "vgmidi")


DATASETS = {
    "thesession": load_thesession,
    "nottingham": load_nottingham,
    "emopia": load_emopia,
    "vgmidi": load_vgmidi,
}


def load(name, limit=None):
    """Yield Tunes for a registered dataset, or raise a clear error if not present."""
    if name not in DATASETS:
        raise SystemExit("unknown dataset %r; known: %s" % (name, ", ".join(DATASETS)))
    root = data_dir(name)
    if not root:
        raise SystemExit(
            "dataset %r not found under data/raw/%s or data/vendor/%s — run data/fetch.sh %s"
            % (name, name, name, name))
    count = 0
    for tune in DATASETS[name](root):
        yield tune
        count += 1
        if limit and count >= limit:
            return
