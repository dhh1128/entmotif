#!/usr/bin/env bash
# entmotif corpus fetcher — download a dataset into data/raw/<name>/ and record its
# provenance (source URL + sha256) so a mining run is reproducible.
#
# LICENSE DISCIPLINE (see data/README.md): data/raw/ is gitignored and NEVER committed.
# Only data/vendor/ (small, permissively-licensed raw corpora) and data/features/
# (derived aggregate statistics) are tracked. This script just makes the local
# download re-runnable; it does not change what is committed.
#
#   ./data/fetch.sh thesession      # one dataset
#   ./data/fetch.sh all             # every permissively-fetchable dataset
#
# Be a good citizen: heavy parsing/zip is wrapped in nice/ionice by the caller; this
# script only downloads. Re-running skips a dataset whose marker file already exists.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW="$ROOT/data/raw"
mkdir -p "$RAW"

log() { printf '[fetch] %s\n' "$*" >&2; }

record() {  # name file url
  local name="$1" file="$2" url="$3"
  local sum; sum="$(sha256sum "$file" | awk '{print $1}')"
  {
    echo "name:   $name"
    echo "url:    $url"
    echo "file:   $(basename "$file")"
    echo "sha256: $sum"
    echo "bytes:  $(stat -c%s "$file")"
  } > "$(dirname "$file")/PROVENANCE.txt"
  log "$name → $file ($sum)"
}

fetch_thesession() {  # CC0 public-domain data dump
  local d="$RAW/thesession"; mkdir -p "$d"
  [ -f "$d/tunes.json" ] && { log "thesession present, skipping"; return; }
  local url="https://raw.githubusercontent.com/adactio/TheSession-data/main/json/tunes.json"
  curl -fsSL "$url" -o "$d/tunes.json"
  record thesession "$d/tunes.json" "$url"
}

fetch_nottingham() {  # ABC folk corpus (public domain melodies)
  local d="$RAW/nottingham"; mkdir -p "$d"
  [ -n "$(ls -A "$d"/*.abc 2>/dev/null || true)" ] && { log "nottingham present, skipping"; return; }
  # The cleaned ABC set is mirrored in several repos; jukedeck's is the common one.
  local base="https://raw.githubusercontent.com/jukedeck/nottingham-dataset/master/ABC_cleaned"
  for f in ashover hpps jigs morris playford reelsa-c reelsd-g reelsh-l reelsm-q reelsr-t reelsu-z slip waltzes xmas; do
    curl -fsSL "$base/$f.abc" -o "$d/$f.abc" || log "skip $f.abc"
  done
  record nottingham "$(ls "$d"/*.abc | head -1)" "$base"
}

fetch_emopia() {  # emotion-labelled pop-piano MIDI (CC BY; verify in data/README.md)
  local d="$RAW/emopia"; mkdir -p "$d"
  [ -n "$(find "$d" -name '*.mid' 2>/dev/null | head -1)" ] && { log "emopia present, skipping"; return; }
  local url="https://zenodo.org/records/5090631/files/EMOPIA_1.0.zip?download=1"
  log "downloading EMOPIA (~5.5 MB MIDI, Zenodo record 5090631, CC BY 4.0) — see data/README.md"
  curl -fL "$url" -o "$d/EMOPIA_1.0.zip"
  ( cd "$d" && unzip -qo EMOPIA_1.0.zip && rm -f EMOPIA_1.0.zip )
  record emopia "$(find "$d" -name '*.mid' | head -1)" "$url"
}

fetch_vgmidi() {  # emotion-labelled game MIDI (verify license in data/README.md)
  local d="$RAW/vgmidi"; mkdir -p "$d"
  [ -n "$(find "$d" -name '*.mid' 2>/dev/null | head -1)" ] && { log "vgmidi present, skipping"; return; }
  local url="https://github.com/lucasnfe/vgmidi/archive/refs/heads/master.zip"
  curl -fL "$url" -o "$d/vgmidi.zip"
  ( cd "$d" && unzip -qo vgmidi.zip && rm -f vgmidi.zip )
  record vgmidi "$(find "$d" -name '*.mid' | head -1)" "$url"
}

target="${1:-all}"
case "$target" in
  thesession) fetch_thesession ;;
  nottingham) fetch_nottingham ;;
  emopia)     fetch_emopia ;;
  vgmidi)     fetch_vgmidi ;;
  all)        fetch_thesession; fetch_nottingham ;;  # the two permissive starters
  *) echo "unknown dataset: $target (thesession|nottingham|emopia|vgmidi|all)" >&2; exit 1 ;;
esac
log "done: $target"
