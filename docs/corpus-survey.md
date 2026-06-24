# Corpus Survey — Mining Human Music into Conditional Distributions

## Purpose

Entmotif is pivoting to mine *human-authored* music corpora into **conditional probability
distributions** (explicitly NOT a neural model) that feed the decision DAG that turns a hash into a
short, hummable motif. This document surveys candidate corpora and feature-extraction toolkits
against the maintainer's priority feature dimensions — motif development/re-articulation, **emotion**,
dynamics, instrument choice + register-per-instrument, meter, contour, groove, harmony, voicing
density — and against entmotif's current engine reality (14 styles, GM program numbers, MIDI
registers, major/minor mode, 4/4-only with meter expansion as a future track, functional harmony).
The license discipline is strict: **vendor + commit only small, permissively-licensed raw corpora;
for everything else, fetch locally via a script and commit only derived aggregate statistics** (which
are not redistribution of the work).

## Method / verification note

All entries were checked against primary sources via web search and direct fetch on **2026-06-24**
(WebSearch + WebFetch + the GitHub licenses/contents API). Per entmotif's AGENTS.md "distrust
unverified claims" mandate, every license verdict cites the URL it was read from. Items I could **not**
confirm from a primary source carry a **`[verify]`** tag. Key methodology note on licenses: GitHub's
license API returns `NOASSERTION` or 404 when no recognized `LICENSE` file exists — I treated a
repo with only a README and no LICENSE file as **all-rights-reserved by default** (the legally correct
reading), and say so explicitly rather than assuming "open because it's on GitHub."

---

## Comparison table

Redistributable column: **vendor** = small + permissive, commit raw into the repo; **fetch-only** =
download locally via a script, commit only derived aggregate stats; **survey-only** = note it exists,
do not pull (license too restrictive or access-gated).

| Dataset | Size | Format | License | Redistributable? | Features afforded (→ entmotif dims) | Priority |
|---|---|---|---|---|---|---|
| **EMOPIA** | 1,087 clips / 387 songs (~315 MB) | MIDI (+ YouTube IDs for audio) | CC BY 4.0 | **fetch-only** (small enough to vendor, but copyrighted pop underneath → derive stats) | **emotion** (Russell 4Q), melody+contour, harmony, dynamics (velocity) | **HIGH** |
| **VGMIDI** | 200 labelled + 3,850 unlabelled | MIDI (piano arr.) | **none / all-rights-reserved** `[verify]` | **survey-only** | emotion (valence-arousal), melody+contour, dynamics | MED |
| **Hooktheory / TheoryTab** | "world's largest" lead-sheet DB | proprietary relative notation; limited chord API | ToS forbids scraping/bulk/TDM/redistribution | **survey-only** (mine nothing without a written data license) | melody+contour, **functional harmony**, **popularity** | survey |
| **Essen Folksong (kern)** | ~8,000+ melodies | **kern (Humdrum) | **copyright, license-restricted** | **survey-only** (do NOT vendor; stats only if license permits — unclear) | melody+contour, **meter (non-4/4)**, phrase/motif structure | MED |
| **Nottingham (jukedeck)** | ~1,000+ tunes | ABC (+ MIDI) | **GPLv3** (repo); some tunes carry third-party IPR | fetch-only (GPLv3 share-alike; derived stats are safer than vendoring) | melody+contour, **meter**, chords, mode | MED |
| **TheSession data dump** | ~50k+ tune settings | ABC + JSON/CSV/SQLite | **ODbL** (not CC0) | **vendor-with-attribution OR fetch-only** (ODbL share-alike attaches) | melody+contour, **meter**, mode, type, **popularity** | **HIGH** |
| **Lakh MIDI (LMD)** | ~176k files | MIDI | CC BY 4.0 (compilation); underlying songs copyrighted | **fetch-only** (never vendor; derive stats) | instrumentation, harmony, groove, voicing density | MED |
| **MetaMIDI (MMD)** | 436,631 files | MIDI + metadata | access-gated (Zenodo request form); underlying copyrighted | **survey-only / fetch-after-approval** | **genre/style**, instrumentation, harmony, groove | MED |
| **POP909** | 909 songs × arrangements | MIDI (3 tracks) + annotations | **MIT** (repo) | fetch-only (MIT is permissive, but built from real pop songs → derive stats) | melody/lead, **harmony**, beat/key, motif (POP909_M ext.) | MED |
| **MAESTRO** | ~198.7 h (v3) | MIDI + audio | **CC BY-NC-SA 4.0** | **fetch-only** (NC blocks vendoring for a tool that may be used commercially) | dynamics (velocity+pedal), classical melody/harmony | LOW–MED |
| **GiantMIDI-Piano** | 10,855 MIDI / 2,786 composers | MIDI (user-transcribed) | CC BY 4.0 (metadata/code) | survey-only (you transcribe from YouTube yourself) | classical melody/harmony, dynamics | LOW |
| **ADL Piano MIDI** | 11,086 pieces | MIDI | **none / all-rights-reserved** `[verify]`; LMD-derived | survey-only | **genre**, piano harmony/voicing | LOW |

---

## Per-dataset detail

### EMOPIA — emotion-labelled pop-piano MIDI  **[HIGH]**
- **Canonical sources:** Zenodo record `10.5281/zenodo.5624519` (https://zenodo.org/records/5624519);
  project page https://annahung31.github.io/EMOPIA/ ; code https://github.com/annahung31/EMOPIA and
  https://github.com/seungheondoh/EMOPIA_cls ; ISMIR 2021 paper
  https://archives.ismir.net/ismir2021/paper/000039.pdf .
- **Size / contents:** 1,087 clips from 387 songs; ~315 MB total. Released files are **transcribed
  MIDI**. Audio is NOT redistributed (copyright) — only YouTube IDs + timestamps are given.
- **Emotion scheme (verified on project page):** Russell's 4-quadrant valence-arousal model:
  - **Q1** High-Valence/High-Arousal — 250 clips (avg 31.9 s)
  - **Q2** Low-Valence/High-Arousal — 265 clips (35.6 s)
  - **Q3** Low-Valence/Low-Arousal — 253 clips (40.6 s)
  - **Q4** High-Valence/Low-Arousal — 310 clips (38.2 s)
- **License verdict:** **CC BY 4.0** (verified on https://zenodo.org/records/5624519). The MIDI is
  redistributable with attribution, BUT it is transcribed from copyrighted pop songs — so the safe
  posture for entmotif is **fetch-only**: download locally, commit only the derived per-quadrant
  conditional stats. This is the single best emotion source because it directly maps emotion → MIDI
  pitch/harmony/dynamics, exactly the conditioning axis entmotif wants.
- **Extension:** **EMOPIA+** (https://zenodo.org/records/13122742) adds extracted lead sheets
  (melody+chords), key-signature corrections for 367 clips, and REMI/functional event encodings —
  even more directly mineable for the harmony + contour dimensions.

### VGMIDI — emotion-labelled game-music MIDI  **[MED]**
- **Source:** https://github.com/lucasnfe/vgmidi (Lucas N. Ferreira); paper "Learning to Generate
  Music with Sentiment", ISMIR 2019, https://arxiv.org/pdf/2103.06125 .
- **Size / contents:** 200 piano-arrangement MIDIs labelled + 3,850 unlabelled (AIIDE22 release);
  the labelled set was annotated by 30 subjects on the **Circumplex (valence-arousal)** model.
- **License verdict:** **`[verify]` — no LICENSE file exists.** GitHub's license API returns 404 and the
  repo root contains only `README.md` (confirmed via `gh api repos/lucasnfe/vgmidi/contents`). Absent
  an explicit license, the default is **all-rights-reserved → survey-only.** Do not vendor or
  redistribute; if used at all, mine locally and contact the author for terms.

### Hooktheory / TheoryTab — lead sheets + functional harmony + popularity  **[survey-only]**
- **Sources:** ToS https://www.hooktheory.com/terms ; chord API docs
  https://www.hooktheory.com/api/trends/docs ; product page https://www.hooktheory.com/theorytab .
- **What it has (very attractive):** the largest collection of crowd-sourced songs analyzed into
  **functional** chords + melody in a relative-notation system, *with popularity signal* — a near-
  perfect match for entmotif's harmony + contour + "which progressions are common" needs.
- **License verdict — the critical one:** the ToS **prohibits** copying, scraping, bulk-downloading,
  text-and-data-mining, or redistributing the TheoryTab database (including for training/fine-tuning
  models) except under an express written data license. There is **no full-data API** — only a limited
  OAuth2 chord-probability API (next-chord probabilities + songs-containing-a-progression).
  **Verdict: survey-only. We may NOT mine or vendor TheoryTab content.** The only sanctioned route is
  the public chord-probability API (which itself returns aggregate stats, not lead sheets) or a
  written data license from Hooktheory. `[verify: exact ToS clause wording — hooktheory.com/terms
  returned HTTP 403 to automated fetch; clauses above are from the indexed search snippet, treat the
  prohibition as authoritative but confirm wording before relying on the chord API.]`

### Essen Folksong Collection (**kern / ESAC)  **[MED]**
- **Sources:** https://github.com/ccarh/essen-folksong-collection ; browser http://kern.ccarh.org/browse?l=essen ;
  ESAC home https://www.esac-data.org/ .
- **Size / contents:** ~8,000+ folk melodies in Humdrum **kern (5,157 German + many other regions);
  the wider ESAC database is ~20,000. Carries **phrase, meter, and contour** annotations and — crucially
  for entmotif — lots of **non-4/4 meters**, directly feeding the future meter-expansion track.
- **License verdict:** **copyright, license-restricted.** The CCARH distribution states the files are
  "protected by copyright and distributed by license only" (per the KernScores/ccarh notice; GitHub
  license API returns `NOASSERTION` for ccarh/essen-folksong-collection). **Verdict: survey-only — do
  NOT vendor.** Deriving aggregate stats locally *may* be permissible but the license is not a clean
  open license, so treat as survey-only until the exact CCARH license text is read. `[verify: I could
  not retrieve the verbatim CCARH license/README text — the README path 404'd and the browse page
  exposed no license block; confirm before any local mining.]`

### Nottingham (jukedeck cleaned ABC)  **[MED]**
- **Sources:** https://github.com/jukedeck/nottingham-dataset ; original ABC http://abc.sourceforge.net/NMD/ .
- **Size / contents:** ~1,000+ British/American folk tunes (jigs, reels, hornpipes) as **ABC with
  chords**; jukedeck normalized chord notation (`Cd`/`Ca`/`C/e`). Original DB by Eric Foxley.
- **License verdict:** repo is **GPLv3** (per README, search-verified). Note GPLv3 is a *software*
  copyleft and some tunes carry third-party IPR (e.g. Ashover collection IPR with Mick Peat). **Verdict:
  fetch-only** — derive stats locally; vendoring GPLv3 content into a differently-licensed tool invites
  share-alike entanglement. **Caveat:** prefer the **ABC** files, not the MIDI conversions (the MIDI
  reportedly mangles repeat structure, e.g. AAAABCBCB vs AABCBCB).

### TheSession.org data dump  **[HIGH — leading vendoring candidate]**
- **Sources:** https://github.com/adactio/TheSession-data ; site download
  https://thesession.org/tunes/download ; API https://thesession.org/api .
- **Size / contents:** tens of thousands of tune *settings* in **ABC**, plus parallel **JSON/CSV** and a
  **SQLite** db (`thesession.db`). Files: tunes, sets, aliases, recordings, events, sessions, and
  **tune_popularity**. Fields include `tune_id`, `setting_id`, `name`, **`type`** (jig/reel/polka…),
  **`meter`**, **`mode`**, and the **`abc`** body. Updated ~weekly.
- **License verdict — pin-pointed:** **ODbL (Open Database License), NOT CC0/public-domain.** A
  `LICENSE.md` (ODbL) was added to the repo on 2020-01-30; downstream projects (e.g. Tunetable) attribute
  it as "made available under the Open Database License (ODbL)" (search-verified; GitHub API reports
  `NOASSERTION` because ODbL isn't in its SPDX auto-detect set, consistent with a hand-added
  `LICENSE.md`). ODbL is a **share-alike + attribution database license**.
  **Verdict: vendorable WITH ODbL attribution + share-alike compliance, OR fetch-only.** Because the ABC
  is pure text and parses with **pure Python**, and the meter/mode/type/popularity fields are exactly
  entmotif's meter + contour + mode + popularity axes, this is the **top permissive text-melody
  candidate**. The license surprise (ODbL, not CC0) means: if we vendor it, we must attribute The Session
  and keep any *derived database* under ODbL — committing derived *aggregate statistics* (our north-star
  approach) is the cleanest path and avoids the share-alike question on entmotif's own code.

### Lakh MIDI Dataset (LMD)  **[MED]**
- **Sources:** https://colinraffel.com/projects/lmd/ ; code https://github.com/craffel/midi-dataset .
- **Size / contents:** ~176k MIDI files scraped from the web, de-duped by MD5. Raffel did not transcribe
  them.
- **License verdict:** the **compilation** is **CC BY 4.0** (attribute Raffel + his 2016 thesis), verified
  on the project page. **But** the underlying files are transcriptions of **copyrighted commercial songs**;
  CC BY covers Raffel's collection/alignment work, not the underlying compositions. **Verdict: fetch-only,
  never vendor** — download locally, derive aggregate stats (instrumentation distributions, GM-program
  co-occurrence, groove/voicing-density priors). 2025 ISMIR work flags copyright/dedup concerns, reinforcing
  the stats-only posture.

### MetaMIDI Dataset (MMD)  **[MED]**
- **Sources:** https://www.metacreation.net/projects/metamidi-dataset ; Zenodo (access-gated)
  https://zenodo.org/records/5142664 ; ISMIR 2021 paper https://archives.ismir.net/ismir2021/paper/000022.pdf .
- **Size / contents:** **436,631** MIDI files; artist/title metadata for 221,504 and **genre** metadata for
  143,868 — plus Spotify/MusicBrainz cross-links. The genre metadata is the draw for entmotif's
  style dimension.
- **License verdict:** **access-gated** — Zenodo requires a request form (name, institution, project, ack).
  Underlying MIDI is copyrighted (authors provide a copyright-meta-events list, not a clean license).
  **Verdict: survey-only now; fetch-after-approval** if the genre-conditioned stats prove worth the
  request. Derive stats only; never vendor.

### POP909  **[MED]**
- **Sources:** https://github.com/music-x-lab/POP909-Dataset ; ISMIR 2020 paper
  https://arxiv.org/abs/2008.07142 .
- **Size / contents:** 909 pop songs, each as MIDI with **MELODY / lead-instrument / piano-accompaniment**
  tracks, plus tempo/beat/key/**chord** annotations. Extensions: POP909-CL (chord labels, CC BY-NC-SA),
  **POP909_M** (motif annotations — directly relevant to entmotif's motif-development axis).
- **License verdict:** repo `LICENSE` is **MIT** (verified verbatim at
  https://github.com/music-x-lab/POP909-Dataset/blob/master/LICENSE — no NC/research-only clause).
  Permissive in principle, but the content derives from real pop songs, so **fetch-only + derive stats** is
  the prudent posture. Note POP909-CL specifically is CC BY-**NC**-SA — don't conflate the two.

### MAESTRO  **[LOW–MED]**
- **Sources:** https://magenta.tensorflow.org/datasets/maestro ;
  https://magenta.withgoogle.com/maestro-wave2midi2wave .
- **Size / contents:** v3 = **198.7 hours** of virtuoso classical piano (Piano-e-Competition), MIDI+audio,
  ~3 ms aligned, with **velocity + sustain/sostenuto/una-corda pedal** — a strong **dynamics** source.
- **License verdict:** **CC BY-NC-SA 4.0** (verified on the Magenta dataset page). The **NC** clause blocks
  vendoring into a tool that may be used commercially, and **SA** would force share-alike on a derived
  database. **Verdict: fetch-only**, and even then derive only NC-safe aggregate dynamics stats; mostly
  classical, so it overlaps entmotif's existing classical/baroque coverage rather than expanding breadth.

### GiantMIDI-Piano  **[LOW]**
- **Source:** https://github.com/bytedance/GiantMIDI-Piano (paper in TISMIR
  https://transactions.ismir.net/articles/10.5334/tismir.80).
- **Size / contents:** 10,855 MIDI of 2,786 classical composers (1,237 h), but **you transcribe them
  yourself** from YouTube via the repo's pipeline (~200 GPU-h). README states license **CC BY 4.0**
  (verified via the repo README "## License → CC BY 4.0") — but that covers metadata/code; the MIDI is
  user-generated from copyrighted recordings. **Verdict: survey-only** (high effort, classical-only,
  low marginal value vs. entmotif's existing classical coverage).

### ADL Piano MIDI  **[LOW]**
- **Source:** https://github.com/lucasnfe/adl-piano-midi .
- **Size / contents:** 11,086 piano pieces organized by **genre/sub-genre/artist**, derived from LMD's
  piano-family tracks + ~2,065 scraped files.
- **License verdict:** **`[verify]` — no LICENSE file** (repo root has only `README.md`, no license text;
  GitHub API 404). LMD-derived (so inherits the copyrighted-underlying issue) and unlicensed →
  **survey-only.**

---

## Feature-extraction toolkits

**jSymbolic 2.2 (jMIR)** — Java, open source (GPL `[verify: jMIR is stated free/open-source; exact GPL
text not read from a primary file]`). Computes **246** features from a MIDI file in eight categories that
map almost one-to-one onto entmotif's priority dimensions: **texture** (≈voicing density), **rhythm**
(≈groove/meter), **dynamics**, pitch statistics, **melodic intervals** (≈contour), **chords/vertical
intervals** (≈harmony/voicing), **instrumentation**, and MEI-specific. Native input is MIDI (kern/MusicXML
support has been a roadmap item). This is the strongest off-the-shelf extractor for the
instrumentation/harmony/dynamics/texture axes — worth reusing rather than re-implementing, but it's a JVM
dependency and entmotif is determinism-strict, so use it offline to *produce stats*, never in the runtime
path. Source: https://github.com/DDMAL/jSymbolic2 , paper http://ismir2018.ircam.fr/doc/pdfs/26_Paper.pdf .

**music21** — Python, **BSD license** (developed *at* MIT, licensed BSD — verified from source headers
"License: BSD"). Parses **ABC, Humdrum/**kern, MusicXML, Musedata, and MIDI** — i.e. *every* text format
in this survey (TheSession ABC, Nottingham ABC, Essen **kern) parses directly. Ships analysis for key/mode,
meter, intervals/contour, chord/roman-numeral (functional) analysis, and more. **This is the recommended
backbone for the pure-Python mining pipeline:** it covers parsing + a lot of the
contour/meter/mode/harmony feature extraction without a JVM, and BSD imposes no copyleft entanglement.
Source: https://music21.org , https://github.com/cuthbertLab/music21 .

**FANTASTIC** — R toolbox by Daniel Müllensiefen (Goldsmiths), "Feature ANalysis Technology Accessing
STatistics In a Corpus." Computes **melodic features on monophonic melodies** — directly relevant to
contour/melody mining of the folk corpora. Caveats: it's R (not Python), works on monophonic input only,
and has a minimum-input-length floor that excludes very short patterns (a concern for entmotif's short
motifs). `[verify: no explicit software-license declaration found — distributed as a Goldsmiths technical
report/toolbox.]` A modern Python package `melody-features` (PyPI) re-implements FANTASTIC + jSymbolic2 +
others (200+ features) and may be the more practical route than shelling to R.
Source: https://www.gold.ac.uk/psychology/staff/mullensiefen/ , PyPI `melody-features`.

**MIDI-emotion models** — for the emotion axis, the EMOPIA and VGMIDI repos ship classifier code
(EMOPIA_cls does MIDI+WAV emotion recognition). These are reference implementations for *mapping MIDI →
Russell quadrant*; for entmotif's inverse goal (quadrant → musical-feature priors) we mine the labelled
corpora directly rather than running the classifiers, so treat these as validation tools, not pipeline
components.

---

## RECOMMENDED VETTED STARTER SET

A concrete, small set we can mine **locally now**, biased toward (a) one emotion-labelled set, (b)
permissive pure-Python-parseable text-melody corpora, with a clear defer list.

1. **TheSession.org data dump (ABC + JSON)** — *primary text-melody corpus.*
   - **License verdict:** **ODbL** — **vendor-with-attribution OR fetch-only.** Cleanest path consistent
     with entmotif's north star: commit only **derived aggregate statistics** (sidesteps ODbL share-alike
     on our codebase) and credit The Session. If we ever vendor raw ABC, we must carry the ODbL notice.
   - **Feeds:** **meter** (incl. non-4/4 — the `type`/`meter` fields), **contour/melody** (ABC body parsed
     by music21), **mode** (major/minor + modal), and **popularity** (the `tune_popularity` table).
   - **Why first:** largest permissive text corpus, pure-Python parse, directly fills the meter-expansion
     and contour/mode/popularity axes.

2. **EMOPIA (+ optionally EMOPIA+)** — *the emotion anchor.*
   - **License verdict:** **CC BY 4.0**, but copyrighted pop underneath → **fetch-only** (download via
     script, commit per-quadrant conditional stats only; attribute the authors).
   - **Feeds:** **emotion** (Russell 4Q valence-arousal — the dimension no other starter set covers),
     plus melody/contour, **harmony** (esp. EMOPIA+ lead sheets), and **dynamics** (MIDI velocity).
   - **Why:** it is the only clean, MIDI-native, emotion-labelled set; emotion is a top-priority axis with
     no substitute in the folk corpora.

3. **Nottingham (jukedeck ABC)** — *secondary text-melody corpus with chords.*
   - **License verdict:** **GPLv3** → **fetch-only** (derive stats locally; avoid vendoring GPLv3 raw text
     into the tool). Prefer the **ABC**, not the MIDI conversions.
   - **Feeds:** **chords/harmony** (cleaned chord notation), **meter**, **contour**, **mode** — complements
     TheSession with explicit chord symbols the session tunes lack.

**Defer (do not pull now):**
- **Essen **kern** — would be ideal for non-4/4 meter + phrase/contour, but it is **copyright/
  license-restricted**; defer until the exact CCARH license is read and stats-derivation is confirmed
  permissible. (`[verify]`)
- **Hooktheory/TheoryTab** — best harmony+popularity data, but **ToS forbids mining/redistribution**;
  pursue only via a written data license or the limited chord-probability API. Do **not** scrape.
- **Lakh / POP909 / MetaMIDI / MAESTRO / GiantMIDI / ADL** — useful for instrumentation/genre/dynamics
  later, but all either copyrighted-underlying (fetch-only, stats only), access-gated (MMD), NC-licensed
  (MAESTRO), or high-effort/unlicensed (GiantMIDI, ADL, VGMIDI). Defer to a second mining wave once the
  text-melody + emotion pipeline (picks 1–3) is proven.

**Toolkit for the starter pipeline:** **music21** (BSD, pure Python) for parsing all three starter
corpora (ABC + MIDI) and extracting meter/mode/contour/harmony; reserve **jSymbolic** for a later
instrumentation/texture pass on MIDI corpora. Keep all extraction **offline** — produce committed
aggregate stats; never put a JVM/R dependency in entmotif's determinism-strict runtime path.
