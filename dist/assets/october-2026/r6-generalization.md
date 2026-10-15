# R6 generalization and failure analysis

| Fit / checkpoint | Regime | Math exact | Coding exact | Physics MSE | Physics MAE |
|---|---|---:|---:|---:|---:|
| r6-p1-raw / initial | final_iid | 0 | 0 | 138.92 | 8.61962 |
| r6-p1-raw / initial | final_ood | 0 | 0 | 4042.21 | 42.2353 |
| r6-p1-raw / best | final_iid | 0.0104167 | 0 | 100.778 | 7.22466 |
| r6-p1-raw / best | final_ood | 0 | 0 | 3919.71 | 41.7243 |
| r6-p1-scaled / initial | final_iid | 0 | 0 | 140.034 | 8.72853 |
| r6-p1-scaled / initial | final_ood | 0 | 0 | 4050.49 | 42.3033 |
| r6-p1-scaled / best | final_iid | 0.0104167 | 0 | 45.7424 | 4.85222 |
| r6-p1-scaled / best | final_ood | 0 | 0 | 3393.04 | 38.5591 |

## Observed output collapse and physical-law failures

Native sequential arithmetic and program semantics have not been demonstrated. The development-selected models repeatedly emit a few answer strings across different protected problems. A rare correct string under this collapse is not evidence of transferable arithmetic. The raw coding model's perfect rename/reformat invariance accompanies constant wrong predictions; it does not establish program understanding.

- r6-p1-raw, mathematics: 1 distinct valid outputs across 192 final cases; answer counts {"-12": 192}; 1 exact answers.
- r6-p1-raw, coding: 1 distinct valid outputs across 192 final cases; answer counts {"12": 192}; 0 exact answers.
- r6-p1-scaled, mathematics: 3 distinct valid outputs across 192 final cases; answer counts {"-12": 106, "-120": 31, "-1200": 55}; 1 exact answers.
- r6-p1-scaled, coding: 2 distinct valid outputs across 192 final cases; answer counts {"12": 25, "120": 167}; 0 exact answers.

These counts come from the verified raw prediction files and include both final regimes. Teacher-forced loss reduction did not produce reliable free-running reasoning.

The physics correction changes conditioning, with the same architecture, seed, cases and update budget. Matched protected state errors improved, but intervention results remain mixed:

| Matched physics measure | Raw selected | Standardized selected |
|---|---:|---:|
| final_iid state MSE | 100.778 | 45.7424 |
| final_ood state MSE | 3919.71 | 3393.04 |
| final_iid/physics/double_time response MSE | 371.043 | 388.917 |
| final_iid/physics/split_time_same_force response MSE | 10.8203 | 10.8762 |

Splitting a constant-force time interval leaves the analytical final state unchanged. Neural predictions changed on 100.0% of raw and 100.0% of corrected IID probes. The residual response errors and worsened double-time response error prevent a physical-law compositionality claim. Average state-error improvement is evidence of better fitted predictions, not recovered mechanics or general STEM reasoning.

*Excerpt from the preserved report. Detailed per-case predictions are omitted from this public summary.*
