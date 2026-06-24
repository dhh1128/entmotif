#!/usr/bin/env bash
# Render the test MIDI through every soundfont in ./sf/ via FluidSynth.
# Usage: ./render_test.sh [path/to/file.mid]   (defaults to test_instruments.mid)
set -euo pipefail
cd "$(dirname "$0")"

MID="${1:-test_instruments.mid}"
[ -f "$MID" ] || { echo "Missing $MID — run: python3 gen_test_midi.py"; exit 1; }
mkdir -p sf

shopt -s nullglob
fonts=(sf/*.sf2 sf/*.sf3)
[ ${#fonts[@]} -gt 0 ] || { echo "No soundfonts in sf/ — see step 2 instructions."; exit 1; }

midbase="$(basename "${MID%.*}")"
for sf in "${fonts[@]}"; do
    name="$(basename "${sf%.*}")"
    out="render_${midbase}__${name}.wav"
    echo ">> $sf -> $out"
    fluidsynth -ni -g 0.8 -F "$out" -r 44100 "$sf" "$MID" >/dev/null
done

echo
echo "Done. Compare these in Audacity (Windows):"
ls -1 render_*.wav
echo "WSL2 path maps to Windows as: \\\\wsl\$\\<distro>\\$(pwd | sed 's#^/##; s#/#\\\\#g')"
