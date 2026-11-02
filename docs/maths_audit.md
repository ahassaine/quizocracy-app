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

Statutory items thin or missing in the existing years (to be added):

* Y3: days in each month / leap years; tenths from dividing by 10; horizontal and vertical lines.
* Y6: shapes with the same area but different perimeters; volume in mm³/km³.

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
