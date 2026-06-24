"""entmotif — turn a high-entropy value into a short, recognizable musical motif.

Deterministic, zero-dependency engine. Public API is assembled here as the
package's modules are extracted from the experiments/engine prototype; until the
refactor completes, the canonical entry points remain :func:`generate`,
:func:`abc_export`, and :func:`write_midi` (re-exported once engine/exporters land).
"""
