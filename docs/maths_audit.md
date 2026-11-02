# Maths bank audit (2 Nov 2026)

Yardstick: the statutory programmes of study, *National curriculum in England: mathematics*
(DfE, KS1–2 by year; KS3 as one stage). Every skill was run 300 times at each of the three
difficulty tiers (`scripts/maths_fuzz.py`), two questions per skill were read by hand with their
answers, and each year's skill list was checked against the statutory bullets for that year.

## What exists

| Year | Skills | Strands | Source |
|---|---|---|---|
| Y3 | 84 | 10 | family app |
| Y4 | 99 | 10 | family app |
| Y6 | 98 | 10 | family app |
| Y8 | 109 | 10 | family app (KS3) |
| Y1, Y2, Y5, Y7, Y9 | none | | Y5 was served Y4, Y7 Y6, Y9 Y8; Y1–2 had no maths |

## Correctness

* No generator crashes; every stored answer is accepted by the checker; no choice list lacks
  its answer (390 skills × 3 tiers × 300 runs).
* Hand reading of 780 questions found no wrong answers. Bugs found and fixed:
  * **Answers sent to the browser** — 5,188 table questions (data and in/out tables) carried the
    true value of the hidden cell in the page data. The engine now blanks it before sending.
    *The family app's engine has the same leak (not touched).*
  * Y4.1.e: "use the number closest to 78 that divides by 4" — 76 and 80 tie. Tie removed.
  * Y4.9.c: "the two largest groups" named the last two groups, not the tallest bars.
  * Y4.0.e (easy tier): "800 = ___ + 0 + 0". Easy tier now has no zero digits.
  * Y8.2.e: mean of identical values ("mean of 2.2, 2.2"). Values now distinct, 3–5 of them.
  * Y8.8.o: "write 238° as a three-figure bearing". Now angles under 100°, answer "072" form.
  * Y8.9.b: "round 68000 to 3 s.f." (already rounded). Now always needs rounding.
  * Y8.9.m: correlation chosen at random for fixed contexts ("ice creams fall as temperature
    rises"). Each context now carries its real correlation.

## Fit to the year

Out-of-year skills (content the curriculum places later) are now left out of their year's
ladder; the later year's bank teaches it (`OUT_OF_YEAR` in `maths_mastery.py`):
Y3.9.f likelihood · Y4.4.j algebraic expressions · Y4.5.f simplest form · Y4.6.i adding
decimals · Y4.7.e imperial units · Y4.9.h probability · Y4.9.i mean · Y6.9.i mode/median ·
Y6.9.j probability.

Statutory items that were missing in the existing years, now added (`y3_gen_d`, `y6_gen_f`):

* Y3.6.k tenths from dividing by 10 · Y3.8.m days in each month, leap years, seconds in a minute ·
  Y3.8.n horizontal and vertical lines.
* Y6.8.r same area, different perimeter · Y6.8.s volume in cm³/m³, extending to mm³/km³.

Other notes: several prompts reuse skill names from the family app's original source as
lead-ins ("Percent of change word problem: …", "Nets of three-dimensional figures: …"); they
read awkwardly and should be rewritten in plain wording as each year is revised.

## Build order (agreed with Ali)

1. This audit and its fixes.
2. Year 5 and Year 7 banks, complete against their programmes of study.
3. Year 1 and Year 2.
4. Year 9 and a KS3 spelling list.

All content is hand-written generators: no model calls at build or serve time.

## Year 5 bank (built 2 Nov 2026)

85 skills in 10 strands (`y5_gen_a`–`e`), each with 4–9 question framings and three tiers.
Coverage against the Year 5 statutory programme:

| Statutory area | Skills |
|---|---|
| Numbers to 1,000,000, powers of 10, negatives, Roman numerals to M and years | 5.0.a–i |
| Compare, order, round to 100,000, estimate and check | 5.1.a–g |
| Add/subtract > 4 digits (written, mental), inverse, multi-step, the equals sign | 5.2.a–f |
| Multiples, factor pairs, common factors, primes to 100, prime factors, squares, cubes | 5.3.a–h |
| Mental ×/÷, short and long multiplication, short division, remainders, ×/÷ 10/100/1000 (whole and decimal), scaling, rates, four operations | 5.4.a–k |
| Equivalent fractions, related denominators, mixed/improper, add/subtract, × whole numbers, fractions of amounts | 5.5.a–j |
| Thousandths, decimals ↔ fractions, rounding, ordering to 3 d.p., decimal problems, per cent and equivalences | 5.6.a–j |
| Metric and imperial units, composite perimeter, area (rectangles, irregular), volume, capacity, time, measure and money problems | 5.7.a–j |
| 3-D from 2-D, estimating/measuring angles, 360°/180°/90° facts, rectangles, regular polygons, reflection, translation | 5.8.a–j |
| Line graphs, tables, timetables | 5.9.a–d |

Not testable on screen: *draw* given angles (measuring with a protractor is covered).
Also fixed while building: the area grid printed the shaded count on "what fraction is shaded"
questions (all years), and numeric angle questions showed an "acute / right / obtuse" hint.

## Year 7 bank (built 2 Nov 2026)

KS3 is a single statutory stage, so Year 7 is the entry layer used by common KS3 schemes; the
existing Year 8 bank carries the deeper KS3 content. 58 skills in 10 strands (`y7_gen_a`–`f`):

| Strand | Skills |
|---|---|
| 7.0 Sequences: term-to-term, position-to-term, nth term, linear/geometric/special, patterns | 5 |
| 7.1 Algebraic notation: writing and reading expressions, substitution, function machines, formulae, vocabulary, × and ÷ of terms | 7 |
| 7.2 Equality & equivalence: one- and two-step equations, forming equations, like terms, single brackets, inequality notation | 6 |
| 7.3 Place value & ordering: any size, =, ≠, <, >, ≤, ≥, decimal places, 1 s.f. and estimation, range and median, standard units | 6 |
| 7.4 Fractions, decimals & percentages: conversion, ordering, one quantity of another, fractions/percentages of amounts, over 100% and change | 5 |
| 7.5 Applications of number: four operations with integers and decimals, priority of operations, mental methods, two-way tables and frequency trees, perimeter/area with decimals | 6 |
| 7.6 Directed number: ordering, four operations, substitution and priority | 4 |
| 7.7 Fractional thinking: add/subtract any fractions and mixed numbers, multiply, divide, problems | 5 |
| 7.8 Lines & angles: notation, angle facts, triangles, quadrilaterals, polygons, parallel/perpendicular and constructions, area of triangles/parallelograms/trapezia, four-quadrant coordinates | 8 |
| 7.9 Sets, probability & data: Venn diagrams, probability scale, sample spaces, primes/HCF/LCM, averages, charts | 6 |

Fixed while building: text answers dropped minus signs ("x>=2" was accepted for "x>=-2", "3n-1" for
"-3n-1"); the normaliser now treats a hyphen as a space only between words.

## Years 1 and 2 (built 2 Nov 2026)

Maths now starts at Year 1 (it used to start at Year 3). Short prompts, pictures first.

* **Year 1** (`y1_gen_a`, 20 skills): counting to 100 forwards and back, numbers to 20 in words,
  counting in 2s/5s/10s, one more/one less, comparing, tens and ones; bonds to 10 and within 20,
  adding/subtracting within 20, missing numbers and the = sign, word problems; equal groups, arrays,
  sharing; halves and quarters; comparing and measuring length, mass, capacity and time, coins and
  notes, days/months/order of events, o'clock and half past; naming 2-D and 3-D shapes, turns and
  position.
* **Year 2** (`y2_gen_a`, 25 skills): counting in 2s/3s/5s/10s, tens and ones, <, > and =, numbers in
  words, odd and even; facts to 20 and related facts to 100, two-digit ± ones/tens/two-digit, three
  one-digit numbers, any order and inverses, problems including change; the 2, 5 and 10 tables,
  × and ÷ statements, problems; 1/3, 1/4, 2/4, 3/4 of shapes and quantities; units and scales,
  comparing measures, money and change, time to five minutes, minutes/hours; properties of 2-D and
  3-D shapes, patterns, turns and direction; pictograms, tally charts, block diagrams and tables.

Not testable on screen: *drawing* clock hands is replaced by setting the clock; making 3-D models.

## Year 9 bank (built 2 Nov 2026)

The upper KS3 layer above the Year 8 bank. 40 skills in 10 strands (`y9_gen_a`–`e`):
zero/negative indices and standard form with negative powers and calculations, roots and surds;
expanding double brackets, factorising quadratics and the difference of two squares, changing
the subject, indices in algebra, algebraic fractions; unknowns on both sides, fractional equations
and x² = k, simultaneous equations, inequalities with negatives; gradients, equations of lines,
quadratic graphs, distance–time and real-life graphs; ratio with differences/totals, direct and
inverse proportion, speed/density/pressure; compound interest and repeated change, reverse
percentages; trigonometry (sides and angles), Pythagoras problems, similar shapes, congruence and
angle reasoning, loci; circles and parts of circles, surface area and volume of prisms and
cylinders, area/volume unit conversion; mutually exclusive events, expected and relative frequency,
Venn and two-way-table probability, independent events; frequency tables, grouped data, comparing
distributions, choosing and criticising charts.

The bank test now also rejects typed numeric answers that cannot be typed exactly (float
artefacts such as 16.666…); one speed question had that defect and is fixed.

**Every year from 1 to 9 now has its own maths bank.**

## KS3 spelling (built 2 Nov 2026)

England has no statutory spelling list after Year 6, so Years 7–9 used to repeat the Year 5–6 list.
`app/data/ks3_spelling.json` now holds three hand-chosen lists — Year 7: 116 words, Year 8: 91,
Year 9: 100 — of commonly misspelt words and subject vocabulary from the KS3 programmes of study
(English, maths, science, geography, history, music, art), UK spellings, none repeating a word from
the NC lists. Homophones (whether, advice/advise, affect/effect, except, stationary/stationery,
licence, personnel, wholly, quiet) get a gap sentence. Audio: Google TTS en-GB Neural2, as for the NC
words (307 clips). `tests/test_spelling_lists.py` checks every year has a list and every word a clip.
