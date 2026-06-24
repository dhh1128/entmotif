# Canon grading — CREATIVE TECHNIQUE lens (Claude faculty, 2026-06-23)

> Per-grader record for the canon calibration pass. Synthesis: `docs/canon-calibration.md`.

## 1. Grades table

| id | letter | /100 | one-line reason (craft on the page) |
|---|---|---|---|
| C01 | A | 94 | Motivic economy: one 4-note cell restated a step lower with a fermata-extended answer — argument from a single germ. |
| C02 | B | 84 | Clean period, but conjunct + literal repetition; variation only at the cadence. |
| C03 | A | 93 | Rocket arpeggio answered by a lyrical descending turn + the run cadence — real contrast inside 8 bars. |
| C04 | B+ | 88 | Gallop cell developed by sequence into the rising charge; the tied fall adds rhythmic interest. |
| C05 | A− | 91 | Master class in transposed sequence: same creeping cell up a third, building tension. |
| C06 | B+ | 87 | Dotted triad-arpeggio call transposed up to high B; expressive `>`/ties, but one idea sequenced. |
| C46 | A− | 90 | Rich dotted-rhythm martial line with varied phrase lengths and constant rhythmic-profile variation. |
| T01 | C+ | 78 | Iconic as sound, but as bare pitch craft just a triadic ascent to a held chord — little development. |
| T02 | B+ | 89 | Mordent + tumbling tuplet descent, transposed to the dominant — genuine ornamental/registral development. |
| C07 | B+ | 88 | Triplet motif sequenced over a pedal; strong, but the B4 F4 frame repeats nearly verbatim. |
| C08 | B | 83 | Accelerating semitone ostinato = rhythmic-diminution device, but two notes as pitch craft. |
| C09 | A− | 90 | Chromatic vamp answered by a contrasting brass phrase — two ideas in dialogue, chromatic color. |
| C10 | B+ | 87 | Two-note call vs answering lyrical minor melody — clear call/response architecture. |
| C11 | A | 94 | Chromatic creep + angular leap + chromatic fall, `=A` voice-leading, rest syncopation — sophisticated chromatic craft. |
| C12 | A− | 91 | 5/4 (3+2) ostinato, transposed answer, contrasting stabbing riff — odd meter + real contrast. |
| T04 | B+ | 88 | Stepwise minor arch with a varied consequent (opens higher, not literal repeat). |
| T05 | A− | 90 | The device IS development: rising-5th restated with the leap opened to an octave — textbook expansion. |
| T07 | A− | 90 | Dotted march cell developed by sequence with `>` as a signature; climbing answer varies contour. |
| C17 | B | 84 | Mild development (the Db extension) but largely the same blues cell; craft is in the groove. |
| C18 | C+ | 78 | Hook stated then repeated verbatim — distinctive but no development as bare melody. |
| C19 | B | 83 | Pedal-E riff with a descending turn; mild contour variation, mostly oscillation over a pedal. |
| C27 | B+ | 87 | Pentatonic call/response with a clear flat3-1-flat7-1 answer + 16th drive — real syncopated craft. |
| C29 | A | 95 | Syncopated 5/4 head with slurred turns, `=A`/`_A` chromatic inflection, sequenced pickup — sophisticated odd-meter jazz. |
| C30 | A− | 91 | Modal bass motif under quartal "So What" answer — call/response, modal harmony, two-voice texture. |
| C31 | B+ | 89 | Leaping figure with D7 #4 color, restated then a varied descending tag — bluesy harmonic interest. |
| C32 | A | 93 | Chromatic descending head with rich b9/b5 ii-V harmony, chromatic passing tones, sequenced 2nd phrase. |
| T29 | A− | 91 | Syncopated leaping RH against a relentless LH boogie — genuine two-voice rhythmic counterpoint. |
| C33 | A | 93 | Chained descending ii-V-I sequences, chromatic approach — sequence done as architecture. |
| C37 | B | 84 | Period with an octave-ish climax, but rote harmony and largely repeated phrase heads. |
| C38 | A− | 91 | Dorian with the raised ^F leading tone, rising-then-descending arc, varied phrase repetition — modal color. |
| C39 | B+ | 87 | Pentatonic arc with a clear climax and varied returns — graceful but harmonically simple. |
| C40 | B+ | 88 | Pentatonic with dotted Scotch-snap rhythms and ties, varied repetition — rhythmic profile carries interest. |
| C49 | B+ | 87 | In-scale (Miyako-bushi) semitone E-F — the modal choice is itself anti-cliché; clean arc. |
| C50 | C+ | 77 | Pleasing 5-note shape but minimal development — a logo, not an argument. |
| T56 | C | 74 | Three descending chimes — perfect signature, essentially zero development as craft. |
| C47 | A− | 90 | Bossa syncopation over a chromatic Fmaj7-G7-Gm7-Gb7 turnaround with tied anticipations — sophisticated. |
| C41 | A− | 91 | Octave-leap opening then wistful descent, rich harmonic frame, varied second phrase. |
| C22 | C | 73 | Eight bars of repeated A then a short scale — almost no development; lives in production/lyrics (CONTROL). |
| C23 | C | 75 | A short pentatonic call repeated nearly verbatim; variation only at the final note (CONTROL). |
| C48 | C+ | 78 | Vamp-driven descending/oscillating line; pleasant contour, little development (CONTROL). |
| C26 | C+ | 78 | Brooding minor-blues with flat color, but mostly repeated E's + a small tag (CONTROL). |
| C21 | C+ | 79 | Broken-chord pedal pattern transposed through changes — harmonically nice, melodically static (CONTROL). |

**Aggregate (creative technique):** anchors B+/A−/A (87–95); controls C/C+ (73–79).

## 2. Calibration check
LOUD flags (ground-truth "expect A across creative" landing sub-A): **C02 Ode to Joy → B (84)** and **C39 Amazing Grace → B+ (87)**, both attribution **(a)** — "simplicity executed perfectly" has little *transformation*, which is exactly what this lens rewards; carried by lyricism/memorability. NOT a rubric bug — the fix is to relabel their ground-truth expectation (lyricism+memorability), not change a rule. Other sub-A− anchors (T01, C08, C17, C18, C50, T56, etc.) all (a), narrow logos/riffs carried by memorability. No (b) (low-confidence files C31/C32 still graded A−/A). No genuine (c).

## 3. Control behavior
Controls cluster C/C+ (73–79); anchors B+/A−/A (87–95). No control reaches anchor territory; the most-developed control (C21, 79) sits below the lowest real-craft anchor. Clean.

## 4. What the high-grading anchors SHARE (creative technique → engine priors)
1. A single germinal cell, then TRANSFORM it (transpose / intervallic expansion / fragment) — not verbatim repeat.
2. Call-and-response of two contrasting ideas inside the phrase.
3. Chromatic voice-leading / color tones as a signature, not decoration.
4. Rhythmic-profile variation + broken/odd rhythm (`>`, tuplets, ties, slurs, 5/4).
5. Sequence as architecture (second half = pitch-shifted derivative).
6. Multi-voice texture where it earns its place (independent rhythmic identity, not parallel doubling).

**Losers' anti-pattern:** verbatim repetition with change only at the final note; static arpeggio/oscillation over a pedal; rote diatonic harmony — exactly what the engine must not default to.
