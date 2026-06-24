"""entmotif CLI — render a demo batch of motifs to .mid files.

Importing this module has no side effects; call :func:`main` (or run
``python -m entmotif.cli``) to write the demo corpus and print a summary table.
"""
from entmotif.engine import generate
from entmotif.theory import KEY_NAMES
from entmotif.exporters.midi import write_midi


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s)[:24].strip("-")


def main():
    demo = ["did:example:alice", "did:example:alife",
            "550e8400-e29b-41d4-a716-446655440000",
            "0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7",
            "GhostKey-2026", "did:example:alice"]
    print("entmotif v0.8 — real motivic transformation (sequence/inversion/fragment/"
          "augment/diminish), developed V:4, unified climax, texture envelope, ties:\n")
    print("  # | input              | key/mode | tempo | lead    | form        | bars "
          "| arr          | fat | res")
    print("  --+--------------------+----------+-------+---------+-------------+------+-"
          "-------------+-----+----")
    for i, v in enumerate(demo, 1):
        notes, m = generate(v)
        write_midi(notes, m["tempo"], m["lead_prog"], m["ans_prog"],
                   "motif_%d_%s.mid" % (i, slug(v)))
        print("  %d | %-18s | %-2s %-5s | %5d | %-7s | %-11s | %4d | %-12s | %3d | %s"
              % (i, v[:18], KEY_NAMES[m["key"]], m["mode"], m["tempo"], m["lead"],
                 m["form"], m["bars"], m["arr"], m["fat"], m["res"]))
    print("\n  #1 vs #2: one-char input change.   #1 vs #6: identical input.")


if __name__ == "__main__":
    main()
