"""entmotif entropy — the fingerprint and the deterministic decision source.

Every musical choice is a pure function of the input's cryptographic fingerprint:
:func:`fingerprint_text` hashes the (normalized) input once, and :class:`Chooser`
derives a fresh independent value per labelled decision by hashing
``fingerprint + label``. This gives avalanche (one-char change -> different motif)
and lets each decision be drawn independently.

SACRED — the label strings passed to Chooser are a FROZEN WIRE FORMAT: they are
hashed to drive output, so they must never change (renaming them silently changes
every motif). Centralizing them as named DecisionKey constants is deferred polish;
for now they live as literals at each call site, unchanged from the prototype.

NOTE (~4eu7 / this.i:81pz4m0v): the prototype fingerprints the RAW input. The real
implementation must normalize and strip prefix/suffix EXACTLY as entviz before
hashing — a pending correctness fix, not part of this behavior-preserving refactor.
"""
import hashlib


def fingerprint_text(value):
    """The motif's entropy source: SHA-512 of the input text (raw, for now)."""
    return hashlib.sha512(value.encode("utf-8")).digest()


class Chooser:
    """Draws independent deterministic decisions from a fingerprint.

    Each method hashes ``fingerprint + label`` so distinct labels yield
    independent draws; the same (fingerprint, label) always yields the same value.
    """

    def __init__(self, fp):
        self.fp = fp

    def v(self, label):
        return int.from_bytes(hashlib.sha512(self.fp + label.encode()).digest(), "big")

    def int(self, label, n):
        return self.v(label) % n

    def choice(self, label, seq):
        return seq[self.v(label) % len(seq)]

    def weighted(self, label, opts, wts):
        """Pick opts[i] with probability wts[i]/sum(wts), via PURE INTEGER math.

        Weights MUST be integers. The threshold ``v(label) % total`` and an
        integer cumulative comparison make the choice byte-identical on every
        platform — no float accumulation, no ``WEIGHT_SCALE`` division (step 17,
        the cross-platform determinism repair)."""
        iw = [int(w) for w in wts]
        total = sum(iw)
        if total <= 0:
            return opts[-1]
        r = self.v(label) % total
        acc = 0
        for o, w in zip(opts, iw):
            acc += w
            if r < acc:
                return o
        return opts[-1]
