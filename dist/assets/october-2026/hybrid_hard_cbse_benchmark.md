# Matched CBSE-style measurements

## Frozen hard campaign: 36 questions, 12 per subject

Hard source freeze: `5d0ab46`; B: `78c5771`. Same questions, official Qwen revision, CPU float32, four Torch threads, deterministic decoding, advisory budget 128 tokens / pretrained answer budget 192, 30-second generation ceiling. All four arms ran sequentially. Questions/references never entered pretrained weights or advisory prompts; only the question was submitted. No fitting occurred. The response spacing was 150 ms, excluded from per-request latency, equal across arms; no retries. **No HTTP errors occurred in this hard campaign.**

| Mode | Math | Physics | Coding | Answers | Consistent worked responses | Warm p50 | Warm p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pretrained only | {'correct': 3, 'count': 12}/12 | {'correct': 0, 'count': 12}/12 | {'correct': 0, 'count': 12}/12 | 3/36 | 2/36 | 3.59s | 10.02s |
| Frozen B | {'correct': 5, 'count': 12}/12 | {'correct': 1, 'count': 12}/12 | {'correct': 8, 'count': 12}/12 | 14/36 | 14/36 | 2.57s | 5.85s |
| C before prose fix | {'correct': 12, 'count': 12}/12 | {'correct': 12, 'count': 12}/12 | {'correct': 12, 'count': 12}/12 | 36/36 | 35/36 | 3.22s | 8.80s |

Native R6: all 36 general CBSE inputs are unsupported by its research schema; comparative accuracy **N/A**. No native neural attempt at equivalent problems is claimed.

Matched hard answer gain: **22/36, +61.11 percentage points** (B 38.89% -> C 100%). Historical B 31/36 belongs to a different easier campaign and is not the denominator for this gain.

The hard set includes chain/quotient derivatives, rational/trigonometric definite integrals with domains, 3x3 matrices and systems, Bayes, an initial-value ODE, three-charge noncollinear fields, resistor bridges/KCL, signed flux and SI conversions, photoelectric stopping potential, nested loops/recursion/exceptions/scope/stacks, quoted inline CSV, joins/HAVING/subqueries/aggregation. Complex new tasks mostly use explicit JSON schemas. This measures bounded structured computation, not unrestricted natural-language understanding or syllabus mastery.

| Topic | B correct | C correct |
|---|---:|---:|
| composite | 3/3 | 3/3 |
| csv | 0/1 | 1/1 |
| definite | 0/3 | 3/3 |
| determinant | 1/1 | 1/1 |
| exception | 0/2 | 2/2 |
| induction | 0/2 | 2/2 |
| matrix | 1/1 | 1/1 |
| multi_charge | 0/4 | 4/4 |
| nested_loops | 2/2 | 2/2 |
| network | 0/3 | 3/3 |
| ode | 0/1 | 1/1 |
| optics | 1/1 | 1/1 |
| photoelectric | 0/2 | 2/2 |
| probability | 0/1 | 1/1 |
| recursion | 2/2 | 2/2 |
| scope | 1/1 | 1/1 |
| simultaneous | 0/2 | 2/2 |
| sql_aggregate | 0/1 | 1/1 |
| sql_join | 2/2 | 2/2 |
| stack | 1/1 | 1/1 |

## Separate final release check after formatter correction

Hard response h11 had correct posterior 1/2 but a misleading unparenthesized equality. It is counted as an incorrect worked response, not hidden. Commit `a23954a` adds fraction grouping and a regression test; solver numbers are unchanged. A **new disjoint 12-question protected release holdout**, four per subject, was locked after that change. No implementation changes followed its lock.

| Mode | Math | Physics | Coding | Answers | Warm p50 | Warm p95 |
|---|---:|---:|---:|---:|---:|---:|
| b | 1/4 | 0/4 | 2/4 | 3/12 | 3.46s | 5.85s |
| c | 4/4 | 4/4 | 4/4 | 12/12 | 3.39s | 7.98s |
| pretrained | 1/4 | 0/4 | 0/4 | 1/12 | 4.20s | 7.49s |

C's release worked responses: **12/12 consistent**. Native: 12 unsupported, comparative accuracy N/A. The prior hard36 was then reused as regression data: release C **36/36**; this is explicitly not fresh evidence. Do not relabel preformatter hard35/36 worked responses as a fresh 36/36 release worked score.

## Reference and review methods

Expected calculus/system/matrix answers were derived independently of application output. Circuits use a separate Fraction Gaussian-elimination reference rather than the application's SymPy inversion. Vector references sum scalar charge components independently. Physics uses explicit SI constants and signs. Programs were traced independently; SQL rows were manually aggregated. Before any hard predictions, reference audit corrected three errors in the test author's draft (determinant, recurrence, exception trace); the lock records them. These were reference preparation errors, not model-derived corrections.

Automated grading uses restricted symbolic equivalence, exact stdout/tables/mappings, and numeric relative tolerance 1e-5 / absolute 1e-8; matrix entries use exact numeric equivalence. Pretrained full prose was separately reviewed because a strict machine extractor missed correct unlabelled answers. Pretrained h02/h04/h05 count as correct; h04's bounded antiderivative is equivalent but its worked evaluation is incomplete. No arbitrary search for the target number was used. Final release pretrained r03 is correct.

“Consistent worked response” checks displayed equations, signs, units, provenance and program/table semantics against references. It does not certify full pedagogical detail: matrix operations and SQL execution have compact method descriptions; trace displays are bounded. Some tool checks reuse the same symbolic engine and are not independent proofs. The reviewer is the implementing agent using separate references/evaluation code, not a second human or blinded research team. Confidence is limited by the small, deliberately targeted task families and related templates.

Physics dimensional-unit correctness on the hard set: B 1/12, C 12/12, pretrained 2/12 (dimension correctness alone can accompany a wrong number). Joint answer accuracy is shown above. Release C physics units: 4/4.

## Regression, refusal and operational checks

Reused historical40: B 31/36 and C 36/36 answers, both 4/4 original refusals, measured in explicitly solver-only mode to isolate routing/tools. Additional bounded safety controls: B 8/10, C 10/10. B incorrectly verifies an empty answer for an unknown coding task and can erase a removable integral domain hole. C rejects both. Unsupported controls are separate from supported-question denominators. Controls include host imports/files, infinite loops, SQL extensions, singular matrices, missing data, invalid separations and domain holes.

Cold model initialization: B 5.387s; C 3.649s. These are one-run cached-file initialization measurements, not fresh-machine or cold-disk speed claims. Observed warm RSS maxima: B 2.83 GB, C 2.99 GB; monitoring began partway through B, so these are not lifetime peaks. Shared machine, existing idle model service, filesystem cache and workload variability limit timing conclusions. C's hard p95 is slower than B; no performance optimization is claimed. It meets the predeclared <=30s and <=max(2*B p95,10s) gate.

Actual release offline proof blocks socket connections, loads pinned local weights, runs real advisory inference plus a verified tool: passed in 7.315s including initialization. Three separate public demo questions also passed with actual model provenance. Native no-site-packages and extension-removal checks passed. Model nine-file hashes and original delivered B hashes match; 1,306 R6 and 90 R6.1 indexed files remain unchanged.

## All failures and limitations

B hard failures: h04–h06, h09–h12, h13–h23, h29–h30, h33, h36. These are missing pathways/routing except h33's falsely verified blank CSV output. C hard answers: none failed; worked text h11 failed and was fixed afterward. Release C: no answer/worked failures. The inherited response-slot release race remains: unpaced clients can receive 429. Use the documented spacing; this is a known loopback API limitation, not silently retried.

Pretrained hard failures:

- h01 (composite): Truncated before a completed evaluated derivative; quotient-rule setup alone does not complete the requested derivative.
- h03 (composite): Missing 2*x chain factor in derivative of (x^2+1)^3.
- h06 (definite): Restates the unevaluated definite integral; no answer.
- h07 (matrix): Inverse matrix entries fail multiplication identity.
- h08 (determinant): Incorrect determinant expansion and truncated arithmetic; no correct completed determinant.
- h09 (simultaneous): Returned (1,2,3) fails supplied equations; reference (2,-1,3).
- h10 (simultaneous): Returned (1,2,3) fails equations; reference (-2,3,1).
- h11 (probability): Confuses total evidence with posterior, and sums the evidence terms incorrectly.
- h12 (ode): Returned 2*t+3 does not satisfy the ODE and initial condition.
- h13 (multi_charge): Misreads microcoulombs as coulombs and positions as radial distances; no completed vector sum.
- h14 (multi_charge): Invented magnitude 3 m, not the supplied-point vector field.
- h15 (multi_charge): Copies point coordinates as a force vector with incorrect dimension.
- h16 (multi_charge): Zero vector at wrong point and incorrect field units.
- h17 (network): Returns source voltage rather than solved bridge-node potential; V dimension only is valid.
- h18 (network): No numerical node voltage.
- h19 (network): Returns resistance rather than node voltage.
- h20 (induction): Computes delta flux only, not average induced emf.
- h21 (induction): Fails millisecond conversion, turn count and Lenz sign.
- h22 (photoelectric): Misreads frequency exponent and provides no stopping potential.
- h23 (photoelectric): General photoelectric equation only; no requested stopping potential.
- h24 (optics): -10.8 cm is outside predeclared 1e-5 relative tolerance for -10.9090909 cm; premature rounding. Length dimension is valid.
- h25 (nested_loops): 0 instead of 18.
- h26 (nested_loops): 0 instead of 10.
- h27 (recursion): 12 instead of 32; incorrect recurrence interpretation.
- h28 (recursion): 17 instead of 31; ignores accumulation through recursion.
- h29 (exception): 1 instead of 7.
- h30 (exception): 9 instead of 70.
- h31 (scope): Final 30,7 and explanation 12,7 both wrong; actual 17,7.
- h32 (stack): 0 instead of 13.
- h33 (csv): Arithmetic sum should be 30, not 19.5; mean 10, not 6.5.
- h34 (sql_join): Wrong groups and means; fails COUNT(*)=2.
- h35 (sql_join): Includes Bala despite score below subject mean.
- h36 (sql_aggregate): Restates aggregate expressions without resulting table.

Earlier parameter-variation auxiliary results and seven unpaced B 429 errors are retained separately; they are not the headline hard comparison. All raw predictions, locks, references and review rationales are in local evidence. Protected question contents and raw model responses are intentionally excluded from GitHub.
