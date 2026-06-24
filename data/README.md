# entmotif corpus data

This tree holds the inputs and outputs of the corpus-mining pipeline
(`tools/mining/`, see `docs/corpus-survey.md` for the dataset survey and
`docs/corpus-mining-findings.md` for what the data says).

## Layout & what is committed

| Dir | Committed? | Contents |
|---|---|---|
| `data/raw/` | **NO** (gitignored) | Datasets downloaded by `fetch.sh`. Never committed — license discipline below. |
| `data/vendor/` | yes | Small, *cleanly permissive*, redistributable raw corpora (currently **empty** — see policy). |
| `data/features/` | **yes** | Derived aggregate statistics (`<dataset>.<feature>.json`). Small, human-auditable. |

## License discipline (the load-bearing rule)

**We commit only derived aggregate statistics, never source corpora**, unless a corpus
is both small *and* under a cleanly permissive, redistribution-allowing license. Derived
histograms/percentiles are not a redistribution of the underlying work, so committing
`data/features/*.json` is clean regardless of the source license. This is the north-star
posture from the survey and `this.i:v8k2m1p0`.

**Why `data/vendor/` is currently empty — a deliberate, license-aware decision.** None
of the vetted starter corpora is cleanly vendorable:

- **TheSession** is **ODbL** (share-alike + attribution database license), *not* CC0.
  Vendoring the raw ABC would attach ODbL share-alike; committing only derived stats
  sidesteps it.
- **Nottingham** (jukedeck mirror) is **GPLv3**, and some tunes carry third-party IPR —
  fetch-only, derive stats.
- **EMOPIA** is **CC BY 4.0** but transcribed from copyrighted pop songs — fetch-only,
  derive stats, attribute the authors.

So the correct outcome of taking licenses seriously is: **vendor nothing raw right now;
mine locally; commit the stats.** `data/vendor/` remains as the documented mechanism for
a future corpus that *is* cleanly permissive (public-domain ABC, CC0 melodies).

## Provenance

`fetch.sh` writes a `PROVENANCE.txt` (source URL + sha256 + byte size) next to every
download, so a mining run is reproducible and the exact bytes are auditable.

## Sources currently wired (see `docs/corpus-survey.md` for full license verdicts)

| Dataset | `fetch.sh` target | License | Posture |
|---|---|---|---|
| TheSession data dump | `thesession` | ODbL | fetch-only, stats committed |
| EMOPIA (pop-piano, emotion-labelled) | `emopia` | CC BY 4.0 | fetch-only, stats committed |
| Nottingham (jukedeck ABC) | `nottingham` | GPLv3 | fetch-only, stats committed |
| VGMIDI (game MIDI, emotion) | `vgmidi` | **no LICENSE → all-rights-reserved** | survey-only; loader exists but do not redistribute |

Attribution for the committed `data/features/` stats:
- *The Session* (https://thesession.org), ODbL.
- *EMOPIA* — Hung et al., ISMIR 2021 (Zenodo record 5090631), CC BY 4.0.
