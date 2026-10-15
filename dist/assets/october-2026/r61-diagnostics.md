# R6.1 collapse root-cause investigation

## Completed result

Zero-update diagnostics locate **weak problem conditioning through a final-state encoder bottleneck, followed by prior-dominated autoregressive decoding**. There is no evidence of target/codec corruption, lost input bytes, disconnected text parameters, incorrect checkpoint loading, or an evaluator that fabricates constant outputs. This is a measured proximate mechanism and a justified intervention target, not proof of a unique ultimate cause or a successful learning recovery.

All diagnostics ran on CPU on the development Mac with **zero optimizer updates**. Forward/backward reachability probes changed no model parameters or buffers. No R6.1 Kaggle job was submitted. The proposed physics follow-up is on hold.

## Evidence separating the domains

Raw math and coding selected checkpoints produce only `-12` and `12` respectively across all 512 training examples/domain, scoring 2/512 each. The normalized checkpoint still scores math 2/512 and coding 1/512, despite lower teacher-forced CE. Training-set failure rules out explaining collapse solely as unseen-case difficulty.

The math training set has 374 distinct answers and entropy 8.3722 bits; coding has 324 distinct answers and entropy 8.1267 bits. The best train-derived constant gets only 5/512 math and 7/512 coding. Collapsed strings are not majority full answers; digit `1`, digit `2`, EOS and sign frequencies can support low-loss answer-prefix priors. This observation is consistent with a shortcut, but does not prove every decoded token was chosen because of its marginal frequency.

R6 uses byte embeddings and a single 48-wide forward GRU for text. Only its last state reaches fusion; structured operands, expression trees, ASTs and binding fields do not enter the model. Numeric graph properties are masked out for math/coding. Input bytes are distinguishable, but essential early information is very weakly coupled to answer loss. Short math strings and longer coding programs therefore require separate interpretation.

For the raw coding checkpoint, changing a loop body binding changes the exact result from 6 to 16 but changes context norm by only about 0.000094; the output stays `12`. Changing the final loop-bound argument changes context by about 0.728 but still produces `12`. Prefix syntax and bindings are especially attenuated relative to suffix arguments. The normalized checkpoint is more input-sensitive but still wrong, and a semantics-preserving rename changes its answer on the example. Math operand/operator changes produce distinct contexts but the same wrong answer. Nonzero context distance alone is not learned semantics.

## Causal probes and correction

The table uses the first16 original training cases/domain, per-byte answer-loss embedding gradients, and the median ratio of mean gradient norm in the first versus last input third. The same frozen checkpoint tensors are used for both pooling modes.

| Checkpoint / domain | Original early/late gradient | Pooled early/late gradient |
|---|---:|---:|
| p1-raw / mathematics | 0.000302618 | 1.21668 |
| p1-raw / coding | 1.2221e-10 | 1.04165 |
| p1-scaled / mathematics | 0.0729634 | 1.15102 |
| p1-scaled / coding | 0.000980179 | 1.23417 |

This intervention demonstrates that final-only aggregation caused the observed gradient attenuation route: supplying all valid recurrent states restores direct early-token gradient access without updating any weights. It does **not** prove the gradients encode the correct arithmetic/program algorithm. In fact both modes score 0/16 on each sampled domain/fit before any retraining.

The corrected model uses a masked mean of the encoder's recurrent output states instead of its final state. It adds no parameters and changes no input bytes, targets, decoder, loss or physical equations. All other R6 components remain the original imported baseline. Masked pooling can dilute useful suffix information and retains a fixed-width bottleneck; it is a candidate intervention, not a universal solution. No extra speculative representation changes were added.

## Optimization and evaluator exclusions

Both historical runs recorded 600 actual updates at LR0.001, nonzero finite text-gradient norms, and reduced teacher-forced CE. Per-parameter selected-vs-initial weight changes and current per-layer gradients are saved. PAD is ignored correctly; manual tokenwise NLL equals worker CE without broadcasting. Text-specific backward excludes expected unused physical graph/head parameters rather than falsely calling those dead text components.

A selected-checkpoint, first16/domain shared-encoder probe finds raw physics gradient norm about21.86 versus math0.415 and coding0.200; normalized physics0.682 versus math0.348 and coding0.328. Raw loss imbalance is a plausible contributor. These are local checkpoint probes, not a reconstruction of the training trajectory; normalized text still collapses, so physics scaling alone was insufficient. The recovery pilot isolates tiny-set text learnability in both matched arms; it is not a physics follow-up.

A second greedy implementation, safe checkpoint reloads, target-blind inference and 768 exact prediction comparisons with the original separate CPU cloud evaluator all agree. Greedy decoding exposes the failed conditional model; there is no evidence that sampling or a solver would establish native reasoning. High teacher-forced token accuracy does not imply correct free-running answers.

## Remaining uncertainty

No fitting is allowed until explicit budget approval. We cannot yet show tiny-set memorization, causally attribute improved accuracy to pooling, determine whether 600 historical updates were enough, or rule out width/optimization/decoder exposure effects. One seed and a narrow gradient sample do not establish generality. The root-cause account is supported at the information-flow level; learning-level sufficiency remains INCONCLUSIVE.

Automated checks: **124 passed in 1.75s**. These checks are not a model-learning score. See R61_DIAGNOSTIC_TESTS.json for explicit PASS/FAIL/INCONCLUSIVE outcomes and diagnostics-final for full measurements.
