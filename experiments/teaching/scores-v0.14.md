# entmotif scores — engine v0.14

Fixed corpus; ABC lead-sheets (melody + chord symbols) for grading.
L:1/16, K:C with explicit accidentals; the C: header gives key/mode/tempo/form. Each score is one input value rendered by the engine.

## Score 1  —  `550e8400-e29b-41d4-a716-446655440000`
(ragtime/happy, E major, 128bpm, aaba, 16 bars, lead=piano, leap=stepwise, arr=lead_counter, fat=2)
```abc
X:1
T:550e8400-e29b-41d4-a716-446655440000
C:entmotif [ragtime] E major, 128bpm, lead=piano, perc=none, form=aaba, arr=lead_counter
M:4/4
L:1/16
Q:1/4=128
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
V:4 name="answer/counter"
K:C
V:1
"E" !mp! =B,2 =A,2 ^C4 =E6 ^D2 | "C#m" =E8 ^C2 =B,2 ^C2 z2 | "F#" !mp! ^F2 =E2 ^G4 ^A6 ^G2 | "B" =A4 ^G4 ^F6 z2 | "E" !mp! =B,2 =A,2 ^C4 =E6 ^D2 | "C#m" =E8 ^C2 =B,2 ^C2 z2 | "F#m" !mp! ^F2 =E2 ^G4 =A6 ^G2 | "B" =E4 =A4 ^F6 z2 | "A" !mf! ^C2 ^D2 ^G4 =E8 | "E" ^G6 z2 =B6 =A2 | "F#m" !f! ^C2 ^D2 ^G4 ^F8 | "B" =B6 z2 ^d6 ^c2 | "E" !mp! ^G2 ^F2 =A4 =B6 =A2 | "C#m" ^c6 z2 ^G2 ^F2 ^G2 z2 | "B" !mf! =B2 =A2 ^c4 ^d6 ^c2 | "E" =A4 ^F4 =E8 |]
V:2
z4 [=E,^G,=B,=D]3 z5 [=E,^G,=B,=D]3 z | z4 [^C=E^G=B]3 z5 [^C=E^G=B]3 z | z4 [^F^A^c=e]3 z5 [^F^A^c=e]3 z | z4 [=B^d^f=a]3 z5 [=B^d^f=a]3 z | z4 [=e^g=b=d']3 z5 [=e^g=b=d']3 z | z4 [^c=e^g=b]3 z5 [^c=e^g=b]3 z | z4 [^f=a^c'=e']3 z5 [^f=a^c'=e']3 z | z4 [=b^d'^f'=a']3 z5 [=b^d'^f'=a']3 z | z4 [=a^c'=e'=g']3 z5 [=a^c'=e'=g']3 z | z4 [=e^g=b=d']3 z5 [=e^g=b=d']3 z | z4 [^f=a^c'=e']3 z5 [^f=a^c'=e']3 z | z4 [=b^d'^f'=a']3 z5 [=b^d'^f'=a']3 z | z4 [=e'^g'=b'=d'']3 z5 [=e'^g'=b'=d'']3 z | z4 [^c'=e'^g'=b']3 z5 [^c'=e'^g'=b']3 z | z4 [=b^d'^f'=a']3 z5 [=b^d'^f'=a']3 z | z4 [=e'^g'=b'=d'']3 z5 [=e'^g'=b'=d'']3 z |]
V:3
=E,,4 z4 =E,,4 z4 | ^C,,4 z4 ^C,,4 z4 | ^F,,4 z4 ^F,,4 z4 | =B,,4 z4 =B,,4 z4 | =E,,4 z4 =E,,4 z4 | ^C,,4 z4 ^C,,4 z4 | ^F,,4 z4 ^F,,4 z4 | =B,,4 z4 =B,,4 z4 | =A,,4 z4 =A,,4 z4 | =E,,4 z4 =E,,4 z4 | ^F,,4 z4 ^F,,4 z4 | =B,,4 z4 =B,,4 z4 | =E,,4 z4 =E,,4 z4 | ^C,,4 z4 ^C,,4 z4 | =B,,4 z4 =B,,4 z4 | =E,,4 z4 =E,,4 z4 |]
V:4
=E,2 ^F,2 ^D,4 =E,6 ^F,2 | =E,8 ^G,2 =A,2 ^G,4 | z16 | z16 | ^G,2 =A,2 ^F,4 =E,6 ^F,2 | =E,8 ^G,2 =A,2 ^G,4 | z16 | z16 | z16 | z16 | z16 | z16 | =B,2 ^C2 =A,4 =E,6 ^F,2 | =E,8 ^G,2 =A,2 ^G,4 | z16 | z16 |]
```

## Score 2  —  `0x742d35cc6634c0532925a3b844bc454e4438f44e`
(march/triumphant, B major, 116bpm, period, 8 bars, lead=oboe, leap=stepwise, arr=call_resp, fat=3)
```abc
X:1
T:0x742d35cc6634c0532925a3b844bc454e4438f44e
C:entmotif [march] B major, 116bpm, lead=oboe, perc=march, form=period, arr=call_resp
M:4/4
L:1/16
Q:1/4=116
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
V:4 name="answer/counter"
K:C
V:1
"B" !mp! =B,2 =E2 =B,4 ^D6 ^A,2 | "G#m" =B,3 ^C ^D4 =B,2 z2 ^C4 | "C#" !mf! =F4 ^F4 =F8 | "F#" =B,4 ^D4 ^C6 z2 | "B" !f! =B =B ^F2 ^A z2 =E ^F2 ^G ^A2 ^F2 ^G | "G#m" =B =B ^F z ^A3 =E ^G2 ^A =B2 ^G2 ^A | "F#" !mf! ^F4 ^G2 z2 ^F8 | "B" =B,2 ^D2 ^C4 =B,8 |]
V:2
z4 [^D^F=A]3 z5 [^D^F=A]3 z | z4 [=B,^D^F]3 z5 [=B,^D^F]3 z | z4 [=F^G=B]3 z5 [=F^G=B]3 z | z4 [^A^c=e]3 z5 [^A^c=e]3 z | z4 [^d^f=a]3 z5 [^d^f=a]3 z | z4 [=B^d^f]3 z5 [=B^d^f]3 z | z4 [^A^c=e]3 z5 [^A^c=e]3 z | z4 [^d^f=a]3 z5 [^d^f=a]3 z |]
V:3
=B,,4 z4 ^F,,4 z4 | ^G,,4 z4 ^D,,4 z4 | ^C,,4 z4 ^G,,4 z4 | ^F,,4 z4 ^C,,4 z4 | =B,,4 z4 ^F,,4 z4 | ^G,,4 z4 ^D,,4 z4 | ^F,,4 z4 ^C,,4 z4 | =B,,4 z4 ^F,,4 z4 |]
V:4
z16 | z16 | ^G2 =B2 ^F4 ^G6 ^D2 | z16 | z16 | z16 | ^F2 =B2 ^F4 ^A2 =B2 ^F4 | z16 |]
```

## Score 3  —  `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
(bossa_nova/peaceful, F# minor, 144bpm, period_tag, 12 bars, lead=nylon-guitar, leap=moderate, arr=call_resp, fat=3)
```abc
X:1
T:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
C:entmotif [bossa_nova] F# minor, 144bpm, lead=nylon-guitar, perc=bossa, form=period_tag, arr=call_resp
M:4/4
L:1/16
Q:1/4=144
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
V:4 name="answer/counter"
K:C
V:1
"F#m" !mp! ^C3 =B, ^C4 ^F8 | "D" =d4 ^G8 ^c4 | "Bm" !mp! ^F4 ^G2 z2 ^F8 | "C#" ^F4 =B4 ^G4 z4 | "F#m" !mf! ^F3 =E ^F4 =A8 | "D" ^f4 =B8 =e4 | "G#dim" !f! =d4 =e2 z2 =d8 | "C#" =A4 ^F4 ^G4 z4 | "F#m" !mp! =A3 ^G =A4 ^c8 | "D" ^f4 =B8 =e4 | "C#" !mf! ^G4 =A2 z2 ^G8 | "F#m" ^c4 =D4 ^F8 |]
V:2
[^F,=A,^C=E]2 z4 [^F,=A,^C=E]2 z2 [^F,=A,^C=E]2 [^F,=A,^C=E]2 z2 | [=D,^F,=A,=C]2 z4 [=D,^F,=A,=C]2 z2 [=D,^F,=A,=C]2 [=D,^F,=A,=C]2 z2 | [=B,=D^F=A]2 z4 [=B,=D^F=A]2 z2 [=B,=D^F=A]2 [=B,=D^F=A]2 z2 | [^C=F^G=B]2 z4 [^C=F^G=B]2 z2 [^C=F^G=B]2 [^C=F^G=B]2 z2 | [^F=A^c=e]2 z4 [^F=A^c=e]2 z2 [^F=A^c=e]2 [^F=A^c=e]2 z2 | [=D^F=A=c]2 z4 [=D^F=A=c]2 z2 [=D^F=A=c]2 [=D^F=A=c]2 z2 | [^G,=B,=D^F]2 z4 [^G,=B,=D^F]2 z2 [^G,=B,=D^F]2 [^G,=B,=D^F]2 z2 | [^C=F^G=B]2 z4 [^C=F^G=B]2 z2 [^C=F^G=B]2 [^C=F^G=B]2 z2 | [^F=A^c=e]2 z4 [^F=A^c=e]2 z2 [^F=A^c=e]2 [^F=A^c=e]2 z2 | [=D^F=A=c]2 z4 [=D^F=A=c]2 z2 [=D^F=A=c]2 [=D^F=A=c]2 z2 | [^C=F^G=B]2 z4 [^C=F^G=B]2 z2 [^C=F^G=B]2 [^C=F^G=B]2 z2 | [^F=A^c=e]2 z4 [^F=A^c=e]2 z2 [^F=A^c=e]2 [^F=A^c=e]2 z2 |]
V:3
^F,,8 ^C,,8 | =D,,8 =A,,8 | =B,,8 ^F,,8 | ^C,,8 ^G,,8 | ^F,,8 ^C,,8 | =D,,8 =A,,8 | ^G,,8 =D,,8 | ^C,,8 ^G,,8 | ^F,,8 ^C,,8 | =D,,8 =A,,8 | ^C,,8 ^G,,8 | ^F,,8 ^C,,8 |]
V:4
z16 | z16 | ^F3 ^G ^F4 =D8 | z16 | z16 | z16 | =d3 ^c =d4 =B8 | z16 | z16 | z16 | ^c3 =B ^c4 =f8 | z16 |]
```

## Score 4  —  `bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4`
(march/tender, G# major, 116bpm, aaba, 16 bars, lead=trombone, leap=moderate, arr=solo_bed, fat=0)
```abc
X:1
T:bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4
C:entmotif [march] G# major, 116bpm, lead=trombone, perc=march, form=aaba, arr=solo_bed
M:4/4
L:1/16
Q:1/4=116
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"G#" !mp! ^G,4 =F2 ^G,2 =C8 | "Fm" ^G,2 =C2 ^C4 =F4 ^G2 z2 | "C#" !mp! ^G,4 =F2 ^G,2 ^C8 | "D#" =C4 ^G,4 ^A,8 | "G#" !mp! ^D2 z2 ^G2 =C2 ^D8 | "Fm" =C2 ^D2 =F4 ^G4 ^G4 | "A#m" !mp! =F2 z2 ^G2 =C2 ^C8 | "D#" ^C4 =C4 ^A,8 | "C#" !mf! ^G,8 ^C4 ^G,2 z2 | "G#" =C2 ^C2 =C2 ^D2 ^G6 z2 | "A#m" !f! ^A,8 ^C4 =C4 | "D#" =G2 ^G2 =F2 ^G2 =G4 z4 | "G#" !mp! =C4 ^G2 =C2 ^D8 | "Fm" =C2 ^D2 =F4 ^G4 ^G2 z2 | "D#" !mf! ^D4 ^G2 =C2 ^D8 | "G#" =C4 ^A,4 ^G,8 |]
V:2
z4 ^D3 z5 ^D3 z | z4 =C3 z5 =C3 z | z4 ^G3 z5 ^G3 z | z4 ^A3 z5 ^A3 z | z4 ^d3 z5 ^d3 z | z4 =c3 z5 =c3 z | z4 =f3 z5 =f3 z | z4 ^a3 z5 ^a3 z | z4 ^g3 z5 ^g3 z | z4 ^d3 z5 ^d3 z | z4 =f3 z5 =f3 z | z4 ^a3 z5 ^a3 z | z4 ^d'3 z5 ^d'3 z | z4 =c'3 z5 =c'3 z | z4 ^a3 z5 ^a3 z | z4 ^d'3 z5 ^d'3 z |]
V:3
^G,,4 z4 ^D,,4 z4 | =F,,4 z4 =C,,4 z4 | ^C,,4 z4 ^G,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^G,,4 z4 ^D,,4 z4 | =F,,4 z4 =C,,4 z4 | ^A,,4 z4 =F,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^C,,4 z4 ^G,,4 z4 | ^G,,4 z4 ^D,,4 z4 | ^A,,4 z4 =F,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^G,,4 z4 ^D,,4 z4 | =F,,4 z4 =C,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^G,,4 z4 ^D,,4 z4 |]
```

## Score 5  —  `01ARZ3NDEKTSV4RRFFQ69G5FAV`
(funk/sad, F# major, 116bpm, aaba, 16 bars, lead=alto-sax, leap=moderate, arr=call_resp, fat=3)
```abc
X:1
T:01ARZ3NDEKTSV4RRFFQ69G5FAV
C:entmotif [funk] F# major, 116bpm, lead=alto-sax, perc=funk, form=aaba, arr=call_resp
M:4/4
L:1/16
Q:1/4=116
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
V:4 name="answer/counter"
K:C
V:1
"F#" !mp! ^F,6 ^D2 ^F,4 =B,4 | "D#m" ^F,2 =B,2 =F,4 ^A,4 =F,2 z2 | "B" !mp! ^F,4 ^G,4 ^F,8 | "C#" ^F,4 ^A,4 ^G,6 z2 | "F#" !mp! ^A,12 ^F4 | "D#m" ^A,8 ^D4 z4 | "G#m" !mp! =B,4 ^C4 =B,8 | "C#" ^A,4 ^F,4 ^G,8 | "B" !mf! ^F,2 z2 ^D2 ^F,2 =B,8 | "F#" ^C3 ^D ^C4 ^A,4 =B,4 | "G#m" !f! ^G,2 z2 =F2 ^G,2 =B,8 | "C#" ^C3 ^F ^C4 =F4 ^C2 z2 | "F#" !mp! ^A,6 ^F2 ^A,4 ^D4 | "D#m" ^A,2 ^D2 ^G,4 ^D4 ^A,2 z2 | "C#" !mf! ^C4 ^D4 ^C8 | "F#" ^G,2 ^F,2 ^A,4 ^F,8 |]
V:2
[^F,^A,^C=E] z2 [^F,^A,^C=E] z2 [^F,^A,^C=E] z2 [^F,^A,^C=E] z2 [^F,^A,^C=E] z [^F,^A,^C=E] z | [^D,^F,^A,^C] z2 [^D,^F,^A,^C] z2 [^D,^F,^A,^C] z2 [^D,^F,^A,^C] z2 [^D,^F,^A,^C] z [^D,^F,^A,^C] z | [=B,^D^F=A] z2 [=B,^D^F=A] z2 [=B,^D^F=A] z2 [=B,^D^F=A] z2 [=B,^D^F=A] z [=B,^D^F=A] z | [^C=F^G=B] z2 [^C=F^G=B] z2 [^C=F^G=B] z2 [^C=F^G=B] z2 [^C=F^G=B] z [^C=F^G=B] z | [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z [^F^A^c=e] z | [^D^F^A^c] z2 [^D^F^A^c] z2 [^D^F^A^c] z2 [^D^F^A^c] z2 [^D^F^A^c] z [^D^F^A^c] z | [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z [^G=B^d^f] z | [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z [^c=f^g=b] z | [=B^d^f=a] z2 [=B^d^f=a] z2 [=B^d^f=a] z2 [=B^d^f=a] z2 [=B^d^f=a] z [=B^d^f=a] z | [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z2 [^F^A^c=e] z [^F^A^c=e] z | [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z2 [^G=B^d^f] z [^G=B^d^f] z | [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z [^c=f^g=b] z | [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z [^f^a^c'=e'] z | [^d^f^a^c'] z2 [^d^f^a^c'] z2 [^d^f^a^c'] z2 [^d^f^a^c'] z2 [^d^f^a^c'] z [^d^f^a^c'] z | [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z2 [^c=f^g=b] z [^c=f^g=b] z | [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z2 [^f^a^c'=e'] z [^f^a^c'=e'] z |]
V:3
^F,,2 z ^F,, z2 ^F,, z ^C,,2 z ^F,, z2 ^C,,2 | ^D,,2 z ^D,, z2 ^D,, z ^A,,2 z ^D,, z2 ^D,,2 | =B,,2 z =B,, z2 =B,, z ^F,,2 z =B,, z2 =B,,2 | ^C,,2 z ^C,, z2 ^C,, z ^G,,2 z ^C,, z2 ^C,,2 | ^F,,2 z ^F,, z2 ^F,, z ^C,,2 z ^F,, z2 ^C,,2 | ^D,,2 z ^D,, z2 ^D,, z ^A,,2 z ^D,, z2 ^D,,2 | ^G,,2 z ^G,, z2 ^G,, z ^D,,2 z ^G,, z2 =B,,2 | ^C,,2 z ^C,, z2 ^C,, z ^G,,2 z ^C,, z2 ^C,,2 | =B,,2 z =B,, z2 =B,, z ^F,,2 z =B,, z2 ^F,,2 | ^F,,2 z ^F,, z2 ^F,, z ^C,,2 z ^F,, z2 ^F,,2 | ^G,,2 z ^G,, z2 ^G,, z ^D,,2 z ^G,, z2 =B,,2 | ^C,,2 z ^C,, z2 ^C,, z ^G,,2 z ^C,, z2 ^C,,2 | ^F,,2 z ^F,, z2 ^F,, z ^C,,2 z ^F,, z2 ^C,,2 | ^D,,2 z ^D,, z2 ^D,, z ^A,,2 z ^D,, z2 ^D,,2 | ^C,,2 z ^C,, z2 ^C,, z ^G,,2 z ^C,, z2 =F,,2 | ^F,,2 z ^F,, z2 ^F,, z ^C,,2 z ^F,, z2 ^F,,2 |]
V:4
z16 | z16 | =B,6 ^F2 =B,4 =F4 | z16 | z16 | z16 | ^G,6 =F2 ^G,4 ^C4 | z16 | z16 | z16 | z16 | z16 | z16 | z16 | ^C6 ^F2 ^G,4 ^C4 | z16 |]
```

## Score 6  —  `GCKFBEIYTKP5RDBQMUTAPDCDHF2TR4LPNRGW4JBQQTQUYZP4LDKP3SGM`
(ragtime/sad, G# minor, 128bpm, period, 8 bars, lead=piano, leap=jumpy, arr=lead_counter, fat=1)
```abc
X:1
T:GCKFBEIYTKP5RDBQMUTAPDCDHF2TR4LPNRGW4JBQQTQUYZP4LDKP3SGM
C:entmotif [ragtime] G# minor, 128bpm, lead=piano, perc=none, form=period, arr=lead_counter
M:4/4
L:1/16
Q:1/4=128
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
V:4 name="answer/counter"
K:C
V:1
"G#m" !mp! =B,2 ^G2 =B,4 ^G6 ^C2 | "E" =B,4 ^G,8 ^C2 z2 | "C#m" !mf! =E2 ^G2 =B,4 ^G6 ^C2 | "D#" ^C4 =B,4 ^A,6 z2 | "G#m" !f! ^G ^G =B,2 ^G3 ^C =B,2 ^G,2 z2 ^C2 | "E" =B, ^G =B,2 ^G3 ^C =B,2 ^G,2 z2 ^C2 | "D#" !mf! ^A,2 ^F2 ^A,4 =G6 =B,2 | "G#m" ^C4 ^A,4 ^G,8 |]
V:2
z4 [^G,=B,^D]3 z5 [^G,=B,^D]3 z | z4 [=E,^G,=B,]3 z5 [=E,^G,=B,]3 z | z4 [^C=E^G]3 z5 [^C=E^G]3 z | z4 [^D=G^A]3 z5 [^D=G^A]3 z | z4 [^G=B^d]3 z5 [^G=B^d]3 z | z4 [=E^G=B]3 z5 [=E^G=B]3 z | z4 [^D=G^A]3 z5 [^D=G^A]3 z | z4 [^G=B^d]3 z5 [^G=B^d]3 z |]
V:3
^G,,4 z4 ^D,,4 z4 | =E,,4 z4 =B,,4 z4 | ^C,,4 z4 ^G,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^G,,4 z4 ^D,,4 z4 | =E,,4 z4 =B,,4 z4 | ^D,,4 z4 ^A,,4 z4 | ^G,,4 z4 ^D,,4 z4 |]
V:4
^D,2 ^C,2 ^A,4 ^D,6 ^A,2 | =B,4 =B,8 ^F,4 | z16 | z16 | ^G,2 ^C,2 ^A,4 ^D,6 ^A,2 | =B,4 =B,8 ^F,4 | z16 | z16 |]
```

## Score 7  —  `bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi`
(reggae/tender, C major, 80bpm, sentence, 4 bars, lead=kalimba, leap=moderate, arr=solo_bed, fat=1)
```abc
X:1
T:bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi
C:entmotif [reggae] C major, 80bpm, lead=kalimba, perc=one_drop, form=sentence, arr=solo_bed
M:4/4
L:1/16
Q:1/4=80
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"C" !mf! =G,2 =D2 =G,4 =C6 =B,2 | "C" =G,4 =A,2 =F,2 =G,4 z4 | "F" !f! =c =c =F2 =B3 =A =F2 =G =E =F2 z2 | "C" =G4 =F4 =C8 |]
V:2
z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 | z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 | z2 [=F=A=c]2 z2 [=F=A=c]2 z2 [=F=A=c]2 z2 [=F=A=c]2 | z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 z2 [=C=E=G]2 |]
V:3
=C,,4 z2 =C,,2 z2 =G,,4 z2 | =C,,4 z2 =C,,2 z2 =G,,4 z2 | =F,,4 z2 =F,,2 z2 =C,,4 z2 | =C,,4 z2 =C,,2 z2 =G,,4 z2 |]
```

## Score 8  —  `EBfdlu8R27Fbx_ehrqwImnK_8Cm79sqbAQ4caaZG_LFv`
(bossa_nova/sad, G# minor, 120bpm, period, 8 bars, lead=clavinet, leap=moderate, arr=solo_bed, fat=2)
```abc
X:1
T:EBfdlu8R27Fbx_ehrqwImnK_8Cm79sqbAQ4caaZG_LFv
C:entmotif [bossa_nova] G# minor, 120bpm, lead=clavinet, perc=bossa, form=period, arr=solo_bed
M:4/4
L:1/16
Q:1/4=120
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"G#m" !mp! ^G,4 ^D2 ^F,2 =B,8 | "E" ^G,8 =B,6 ^G,2 | "C#m" !mf! ^C2 z2 ^G2 =B,2 =E8 | "D#" =B,4 ^G,4 ^A,6 z2 | "G#m" !f! ^G2 ^G =B, =E4 =B,2 z2 ^D3 =B, | "E" ^G,2 ^D ^F, =B,4 ^G,2 z2 =B,3 ^G, | "C#m" !mf! =E4 ^G2 =B,2 =E8 | "G#m" =E4 ^C4 ^G,8 |]
V:2
[^G,=B,^D^F]2 z4 [^G,=B,^D^F]2 z2 [^G,=B,^D^F]2 [^G,=B,^D^F]2 z2 | [=E,^G,=B,=D]2 z4 [=E,^G,=B,=D]2 z2 [=E,^G,=B,=D]2 [=E,^G,=B,=D]2 z2 | [^C=E^G=B]2 z4 [^C=E^G=B]2 z2 [^C=E^G=B]2 [^C=E^G=B]2 z2 | [^D=G^A^c]2 z4 [^D=G^A^c]2 z2 [^D=G^A^c]2 [^D=G^A^c]2 z2 | [^G=B^d^f]2 z4 [^G=B^d^f]2 z2 [^G=B^d^f]2 [^G=B^d^f]2 z2 | [=E^G=B=d]2 z4 [=E^G=B=d]2 z2 [=E^G=B=d]2 [=E^G=B=d]2 z2 | [^C=E^G=B]2 z4 [^C=E^G=B]2 z2 [^C=E^G=B]2 [^C=E^G=B]2 z2 | [^G,=B,^D^F]2 z4 [^G,=B,^D^F]2 z2 [^G,=B,^D^F]2 [^G,=B,^D^F]2 z2 |]
V:3
^G,,8 ^D,,8 | =E,,8 =B,,8 | ^C,,8 ^G,,8 | ^D,,8 ^A,,8 | ^G,,8 ^D,,8 | =E,,8 =B,,8 | ^C,,8 ^G,,8 | ^G,,8 ^D,,8 |]
```

## Score 9  —  `did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK`
(tango/happy, C# minor, 116bpm, period, 8 bars, lead=harmonica, leap=stepwise, arr=solo_bed, fat=2)
```abc
X:1
T:did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
C:entmotif [tango] C# minor, 116bpm, lead=harmonica, perc=none, form=period, arr=solo_bed
M:4/4
L:1/16
Q:1/4=116
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"C#m" !mp! ^C3 =E ^C4 ^G,8 | "A" =A,4 ^G,4 =A,2 ^G,2 =A,2 z2 | "F#m" !mf! =A3 ^c =A4 ^F8 | "G#" ^C4 ^F4 ^D6 z2 | "C#m" !f! ^c2 ^c =A2 =E2 z2 ^F2 =E2 ^F =E ^F | "A" =E2 ^G =E2 =B,2 z2 ^C2 =B,2 ^C =B, ^C | "G#" !mf! ^G3 =B ^G4 ^D6 z2 | "C#m" ^D2 ^C2 =E4 ^C8 |]
V:2
z4 [^C=E^G=B]3 z5 [^C=E^G=B]3 z | z4 [=A,^C=E=G]3 z5 [=A,^C=E=G]3 z | z4 [^F,=A,^C=E]3 z5 [^F,=A,^C=E]3 z | z4 [^G,=C^D^F]3 z5 [^G,=C^D^F]3 z | z4 [^C=E^G=B]3 z5 [^C=E^G=B]3 z | z4 [=A,^C=E=G]3 z5 [=A,^C=E=G]3 z | z4 [^G,=C^D^F]3 z5 [^G,=C^D^F]3 z | z4 [^C=E^G=B]3 z5 [^C=E^G=B]3 z |]
V:3
^C,,6 ^C,,2 ^G,,4 ^G,,4 | =A,,6 =A,,2 =E,,4 =E,,4 | ^F,,6 ^F,,2 ^C,,4 ^C,,4 | ^G,,6 ^G,,2 ^D,,4 ^D,,4 | ^C,,6 ^C,,2 ^G,,4 ^G,,4 | =A,,6 =A,,2 =E,,4 =E,,4 | ^G,,6 ^G,,2 ^D,,4 ^D,,4 | ^C,,6 ^C,,2 ^G,,4 ^G,,4 |]
```

## Score 10  —  `addr1q9c0sj9wp29txqlt0qkc4cz76d5szl4xqgmgpw70ay9zkmskq7stm5kkjjjvrjz9p3kgxx0plzkphkn2yepg6w2zjphshtm0rl`
(blues/tender, G major, 108bpm, aaba, 16 bars, lead=harmonica, leap=moderate, arr=solo_bed, fat=3)
```abc
X:1
T:addr1q9c0sj9wp29txqlt0qkc4cz76d5szl4xqgmgpw70ay9zkmskq7stm5kkjjjvrjz9p3kgxx0plzkphkn2yepg6w2zjphshtm0rl
C:entmotif [blues] G major, 108bpm, lead=harmonica, perc=shuffle, form=aaba, arr=solo_bed
M:4/4
L:1/16
Q:1/4=108
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"G" !mp! =B,6 =E2 =G,4 =A,4 | "Em" =B,4 =A,2 =G,2 =B,6 z2 | "C" !mp! =C6 ^F2 =G,4 =A,4 | "D" =G,4 =B,4 =A,4 z4 | "G" !mp! =G6 =G2 =B,4 =C4 | "Em" =E4 =D2 =C2 =E4 z4 | "Am" !mp! =E6 =G2 =C4 =D4 | "D" =B,4 =G,4 =A,4 z4 | "C" !mf! =C4 =G,4 =C8 | "G" =D4 =C4 =D2 =C2 =E4 | "Am" !f! =A,2 z2 =C4 =A,8 | "D" =D4 =E4 =D2 =B,2 =D2 z2 | "G" !mp! =G,6 =C2 =G,4 =A,4 | "Em" =B,4 =A,2 =G,2 =B,6 z2 | "D" !mf! ^F6 =G2 =A,4 =B,4 | "G" =D4 =G,4 =G,8 |]
V:2
z4 [=G,=B,=D=F]2 z6 [=G,=B,=D=F]2 z2 | z4 [=E,=G,=B,=D]2 z6 [=E,=G,=B,=D]2 z2 | z4 [=C=E=G^A]2 z6 [=C=E=G^A]2 z2 | z4 [=D^F=A=c]2 z6 [=D^F=A=c]2 z2 | z4 [=G=B=d=f]2 z6 [=G=B=d=f]2 z2 | z4 [=E=G=B=d]2 z6 [=E=G=B=d]2 z2 | z4 [=A=c=e=g]2 z6 [=A=c=e=g]2 z2 | z4 [=d^f=a=c']2 z6 [=d^f=a=c']2 z2 | z4 [=c=e=g^a]2 z6 [=c=e=g^a]2 z2 | z4 [=G=B=d=f]2 z6 [=G=B=d=f]2 z2 | z4 [=A=c=e=g]2 z6 [=A=c=e=g]2 z2 | z4 [=d^f=a=c']2 z6 [=d^f=a=c']2 z2 | z4 [=g=b=d'=f']2 z6 [=g=b=d'=f']2 z2 | z4 [=e=g=b=d']2 z6 [=e=g=b=d']2 z2 | z4 [=d^f=a=c']2 z6 [=d^f=a=c']2 z2 | z4 [=g=b=d'=f']2 z6 [=g=b=d'=f']2 z2 |]
V:3
=G,,4 =D,,4 =E,,4 =D,,4 | =E,,4 =B,,4 ^C,,4 =B,,4 | =C,,4 =G,,4 =A,,4 =G,,4 | =D,,4 =A,,4 =B,,4 =A,,4 | =G,,4 =D,,4 =E,,4 =D,,4 | =E,,4 =B,,4 ^C,,4 =B,,4 | =A,,4 =E,,4 ^F,,4 =E,,4 | =D,,4 =A,,4 =B,,4 =A,,4 | =C,,4 =G,,4 =A,,4 =G,,4 | =G,,4 =D,,4 =E,,4 =D,,4 | =A,,4 =E,,4 ^F,,4 =E,,4 | =D,,4 =A,,4 =B,,4 =A,,4 | =G,,4 =D,,4 =E,,4 =D,,4 | =E,,4 =B,,4 ^C,,4 =B,,4 | =D,,4 =A,,4 =B,,4 =A,,4 | =G,,4 =D,,4 =E,,4 =D,,4 |]
```

## Score 11  —  `ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDSD+oM4kLidAptE5pjRA8OBIWNysc9reQJjKegek2jATA3bSvKdq/wdQtpbihEx5OlKMo//V/8QpAIjCSsBaMb6G/e/D5kC9wCjnYJJ68+34L+H5Fx1Ofuiz3BidgssINw/qbV0u1vrCop+ggs6lkl+pIwa+9kPriD9xdowCOQABMVl4todcojY8gZK/Zs5XTwKi9Z8MRS/37FEPxlvpRExMmQU8v2tnP/TDqhR13NSyCZWqiH2ojMNDm2jWR+W65gIjFz4kNsu4EaSNOfKY4U7VRBLXg7om3pvIoarhBFMZvTPQ9FqJU/08BJ/A1tCjCIAY0+zGAAvfRHQt5R2wZXl83n9Xh+9IukW5r/pynpdLx1+WyAOKLxIUKflTWaIcYKBqmfaxz64Gm2lDbF0+9r/0Xf//P8TFDWFo9bo4loIukgjtwQmp8Kn6ngEKj8gS3vLApZ3wN18q3emtglyQEmO+9VXckK4NPOqAzwOu7rQbr7oEPS6HrnY3PKe9JD570= alice@workstation`
(salsa/tender, C# minor, 168bpm, sentence, 4 bars, lead=trumpet, leap=jumpy, arr=solo_bed, fat=2)
```abc
X:1
T:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDSD+oM4kLidAptE5pjRA8OBIWNysc9reQJjKegek2jATA3bSvKdq/wdQtpbihEx5OlKMo//V/8QpAIjCSsBaMb6G/e/D5kC9wCjnYJJ68+34L+H5Fx1Ofuiz3BidgssINw/qbV0u1vrCop+ggs6lkl+pIwa+9kPriD9xdowCOQABMVl4todcojY8gZK/Zs5XTwKi9Z8MRS/37FEPxlvpRExMmQU8v2tnP/TDqhR13NSyCZWqiH2ojMNDm2jWR+W65gIjFz4kNsu4EaSNOfKY4U7VRBLXg7om3pvIoarhBFMZvTPQ9FqJU/08BJ/A1tCjCIAY0+zGAAvfRHQt5R2wZXl83n9Xh+9IukW5r/pynpdLx1+WyAOKLxIUKflTWaIcYKBqmfaxz64Gm2lDbF0+9r/0Xf//P8TFDWFo9bo4loIukgjtwQmp8Kn6ngEKj8gS3vLApZ3wN18q3emtglyQEmO+9VXckK4NPOqAzwOu7rQbr7oEPS6HrnY3PKe9JD570= alice@workstation
C:entmotif [salsa] C# minor, 168bpm, lead=trumpet, perc=salsa, form=sentence, arr=solo_bed
M:4/4
L:1/16
Q:1/4=168
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"C#m" !mf! ^G,2 ^F,6 ^C4 ^F,4 | "C#m" ^G,8 ^C6 ^D2 | "G#" !f! =c =A z2 ^c ^c =B3 ^c ^c =B3 ^c ^c | "C#m" ^F2 z2 ^D4 ^C8 |]
V:2
^C2 =E2 z2 ^G2 =B2 z2 ^G2 =E2 | ^C2 =E2 z2 ^G2 =B2 z2 ^G2 =E2 | ^G,2 =C2 z2 ^D2 ^F2 z2 ^D2 =C2 | ^C2 =E2 z2 ^G2 =B2 z2 ^G2 =E2 |]
V:3
^C,,4 z2 ^C,,2 z2 ^G,,2 ^C,,4 | ^C,,4 z2 ^C,,2 z2 ^G,,2 ^C,,4 | ^G,,4 z2 ^G,,2 z2 ^D,,2 =C,,4 | ^C,,4 z2 ^C,,2 z2 ^G,,2 ^C,,4 |]
```

## Score 12  —  `04d3e8850e766ea1e6999a20f3bff1ded648f014e3c4eee3c17905ada8895ec8b2d17670695211946e4da19982423e654ec8b3576a404b0082130a0e1c3e66e550f41bbb0c1957d041444a5aa992f005aa9693cc90796bcaa5e5ea3ac9e2e93d45889718f1cce931711f461632ae514ba3370a5f553de0dfab83bc7f98f98585414aaf6ffe15d652c5ba62b97f064677987e15298b172e8a58267fe2a9b4a711d5036786f546e48b2549ebeac9490a8a96ef0a01172b0dab37670df15d75adf938bc14d134ce1eed831ff4c29a1b2468da59da4b467d80cd07447ab16b9c439e80c1ad41e3a60fef3a4b8263d9e18b406cd5085d3bc2d779db94c5e4342fcc4874b3ad3744a5e0dc7137bb43f1f4cb6009117b1903c4d4a282c0cd0e805cadebe5b4c3a22807bee2bacbe8a60f7c136b65d645fcbe51bd0bc34e8495cf9ad1289c6a39fddecb2d219632dee9d3efdf002e42a17d5937b6d9328d5edb329a876ae02fc2f9588d5fe8ce1a1e7cdcc2a979363c11edf407d7bac71fcb348646c24f`
(gospel/sad, G major, 84bpm, aaba, 16 bars, lead=trumpet, leap=moderate, arr=solo_bed, fat=3)
```abc
X:1
T:04d3e8850e766ea1e6999a20f3bff1ded648f014e3c4eee3c17905ada8895ec8b2d17670695211946e4da19982423e654ec8b3576a404b0082130a0e1c3e66e550f41bbb0c1957d041444a5aa992f005aa9693cc90796bcaa5e5ea3ac9e2e93d45889718f1cce931711f461632ae514ba3370a5f553de0dfab83bc7f98f98585414aaf6ffe15d652c5ba62b97f064677987e15298b172e8a58267fe2a9b4a711d5036786f546e48b2549ebeac9490a8a96ef0a01172b0dab37670df15d75adf938bc14d134ce1eed831ff4c29a1b2468da59da4b467d80cd07447ab16b9c439e80c1ad41e3a60fef3a4b8263d9e18b406cd5085d3bc2d779db94c5e4342fcc4874b3ad3744a5e0dc7137bb43f1f4cb6009117b1903c4d4a282c0cd0e805cadebe5b4c3a22807bee2bacbe8a60f7c136b65d645fcbe51bd0bc34e8495cf9ad1289c6a39fddecb2d219632dee9d3efdf002e42a17d5937b6d9328d5edb329a876ae02fc2f9588d5fe8ce1a1e7cdcc2a979363c11edf407d7bac71fcb348646c24f
C:entmotif [gospel] G major, 84bpm, lead=trumpet, perc=backbeat, form=aaba, arr=solo_bed
M:4/4
L:1/16
Q:1/4=84
V:1 name="lead"
V:2 name="comp"
V:3 name="bass"
K:C
V:1
"G" !mp! =G,6 ^F,2 =B,4 ^F,4 | "Em" =B,2 =D2 =A,2 =D2 =G,6 z2 | "A" !mp! =A,6 =G,2 ^C4 =G,4 | "D" =G,4 =B,4 =A,6 z2 | "G" !mp! =B,6 =C2 =G,4 =C4 | "Em" =G,2 ^F,2 =B,2 ^F,2 =B,2 z6 | "Am" !mp! =C6 =B,2 =E4 =B,4 | "D" =C4 =B,4 =A,6 z2 | "C" !mf! =G,2 =E2 ^F4 =C8 | "G" =G2 =D2 =G4 =D4 z4 | "Am" !f! =A,2 ^F2 =G4 =E8 | "D" =D2 =E2 =G4 ^F8 | "G" !mp! =D10 z2 =C4 | "Em" =G8 =E8 | "D" !mf! =D6 =C2 ^F4 =C4 | "G" =C4 =A,2 z2 =G,8 |]
V:2
[=G,=B,=D=F]4 z2 [=G,=B,=D=F]2 z2 [=G,=B,=D=F]6 | [=E,=G,=B,=D]4 z2 [=E,=G,=B,=D]2 z2 [=E,=G,=B,=D]6 | [=A,^C=E=G]4 z2 [=A,^C=E=G]2 z2 [=A,^C=E=G]6 | [=D^F=A=c]4 z2 [=D^F=A=c]2 z2 [=D^F=A=c]6 | [=G=B=d=f]4 z2 [=G=B=d=f]2 z2 [=G=B=d=f]6 | [=E=G=B=d]4 z2 [=E=G=B=d]2 z2 [=E=G=B=d]6 | [=A=c=e=g]4 z2 [=A=c=e=g]2 z2 [=A=c=e=g]6 | [=d^f=a=c']4 z2 [=d^f=a=c']2 z2 [=d^f=a=c']6 | [=c=e=g^a]4 z2 [=c=e=g^a]2 z2 [=c=e=g^a]6 | [=G=B=d=f]4 z2 [=G=B=d=f]2 z2 [=G=B=d=f]6 | [=A=c=e=g]4 z2 [=A=c=e=g]2 z2 [=A=c=e=g]6 | [=d^f=a=c']4 z2 [=d^f=a=c']2 z2 [=d^f=a=c']6 | [=g=b=d'=f']4 z2 [=g=b=d'=f']2 z2 [=g=b=d'=f']6 | [=e=g=b=d']4 z2 [=e=g=b=d']2 z2 [=e=g=b=d']6 | [=d^f=a=c']4 z2 [=d^f=a=c']2 z2 [=d^f=a=c']6 | [=g=b=d'=f']4 z2 [=g=b=d'=f']2 z2 [=g=b=d'=f']6 |]
V:3
=G,,4 =B,,4 =D,,4 =D,,4 | =E,,4 =G,,4 =B,,4 =E,,4 | =A,,4 ^C,,4 =E,,4 ^C,,4 | =D,,4 ^F,,4 =A,,4 =D,,4 | =G,,4 =B,,4 =D,,4 =D,,4 | =E,,4 =G,,4 =B,,4 =E,,4 | =A,,4 =C,,4 =E,,4 =C,,4 | =D,,4 ^F,,4 =A,,4 =D,,4 | =C,,4 =E,,4 =G,,4 =G,,4 | =G,,4 =B,,4 =D,,4 =G,,4 | =A,,4 =C,,4 =E,,4 =C,,4 | =D,,4 ^F,,4 =A,,4 =D,,4 | =G,,4 =B,,4 =D,,4 =D,,4 | =E,,4 =G,,4 =B,,4 =E,,4 | =D,,4 ^F,,4 =A,,4 ^F,,4 | =G,,4 =B,,4 =D,,4 =G,,4 |]
```
