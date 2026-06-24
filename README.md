# entmotif
Entmotif is a simple way to turn values with high entropy &mdash; cryptographic keys and signatures, UUIDs, blockchain payment addresses, and so forth &mdash; into a short musical fragment, so a human can compare them by listening. The goal is to help an untrained adult with average musical sensibilities to decide whether two chunks of entropy are the same or different.

Compare [entviz](https://dhh1128.github.io/entviz), which turns entropy into a visual picture.

## Sources of bits
1. the entropy, read beginning to end and end to beginning.
1. the entropy as a grid, reading down and up, either from left to right or right to left
1. the entropy as a grid, reading down-right diagonal, up-right, up-left, down-left

## Questions
1. major or minor key? (1 bit)
1. start octave (2 bits) -> whether bias is to rise, fall, or stay steady
1. convergent or divergent melody (not the right term -- how jumpy is it)?
1. chord progression, duration of each chord (1 measure, 2, 1/2)
1. start note (tonic or 5)
1. time signature (4/4, 3/4, 6/8)
1. rhythm
1. instruments (lead, harmony, rhythm)
1. pitch of individual notes
1. Need some kind of recurring patterns - in rhythm, in notes. Need to investigate compression and other transformation techniques. Need prototypes for call and answer from the motif, and 

    Analyze this as quantities of time, like denominator in time signature. Allows to break into individual notes. Allows us to deal with stressed or unstressed parts of each measure.

1. duration of individual notes

## Instruments
piano - melody, harmony
voice - melody, harmony
trumpet - melody
guitar (or bass, if low) or harp or sitar
marimba or xylophone or triangle
drums, cymbals (need to investigate how rhythm is used)
violin, cello, bass
oboe or clarinet or flute

## Chord progressions

The resolution of a chord progression refers to how it creates a sense of finality or completion within a musical phrase or section. Some chord progressions end with a strong sense of resolution, while others leave the listener with a feeling of anticipation or tension, prompting further musical development. Let's analyze the resolution characteristics of the chord progressions listed:

I - IV - V - I: Resolves strongly to the tonic (I) chord, providing a sense of completion.
I - vi - IV - V: The resolution is moderate, especially when returning to the tonic (I) chord at the end.
I - V - vi - IV: Ends on the subdominant (IV) chord, leaving some sense of openness or anticipation.
vi - IV - I - V: Similar to the previous progression, with a moderate level of resolution when returning to the tonic (I) chord.
I - V - vi - iii - IV - I - IV - V: Strong resolution when returning to the tonic (I) chord.
I - IV - vi - V - I: Strong resolution to the tonic (I) chord at the end.
I - IV - vii° - iii - vi - ii - V - I: Strong resolution to the tonic (I) chord at the end, especially after the dominant (V) chord.
I - IV - ii - V: Moderate resolution when returning to the tonic (I) chord.
I - vi - ii - V: Moderate resolution, especially when resolving to the tonic (I) chord at the end.
I - vi - iii - IV: Ends on the subdominant (IV) chord, leaving some sense of openness.
I - V - vi - IV - IV - V - I: Strong resolution when returning to the tonic (I) chord at the end.
I - iii - IV - V: Ends on the dominant (V) chord, leaving some sense of anticipation.
I - ii - IV - V: Moderate resolution, especially when resolving to the tonic (I) chord at the end.
vi - ii - V - I: Strong resolution to the tonic (I) chord at the end.
I - V - IV - V: Ends on the dominant (V) chord, leaving some sense of anticipation.
I - IV - vii° - iii - vi - ii - V - I: Strong resolution to the tonic (I) chord at the end.
In summary, while some of these chord progressions end with a strong sense of resolution to the tonic (I) chord, others leave the listener with varying degrees of openness or anticipation. The resolution characteristics can also be influenced by factors such as instrumentation, melodic context, and rhythmic treatment within a specific musical composition.
