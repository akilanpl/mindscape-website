# R6 cloud training results

Two completed FP32 CUDA fits; **1200 actual optimizer updates**. Measured fitting/measurement time totals 45.4431 seconds (0.012623 device-hours); this excludes provisioning and is not the provider's billed/quota wall-clock total. Two T4 devices are separate memories; each fit selected cuda:0.

| Fit | Updates | Best dev step | Seconds | Parameters | Peak allocated bytes | Selected checkpoint SHA256 |
|---|---:|---:|---:|---:|---:|---|
| p1-raw | 600 | 400 | 22.8886 | 54014 | 84421632 | b2f3a3f2f0270869b8e9494fb502a36dc31629b1574a9e4755559f063200fd36 |
| p1-scaled | 600 | 600 | 22.5544 | 54014 | 84421632 | 2d2573c5fdf1caea008cc6aad03de6aedf44fa57f0aa5bbd924ee61bc9cdda4d |

Both runs executed 600 updates under the same predeclared development-selection policy. The selected raw checkpoint is step 400; the standardized checkpoint is step 600. Equal run budgets therefore do not imply equal selected-checkpoint training steps. This comparison is a one-seed conditioning experiment, not an architecture ranking.

*Excerpt from the preserved report. Detailed per-case predictions are omitted from this public summary.*
