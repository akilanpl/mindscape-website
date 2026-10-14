# /mind/ announcement review

Review-only route; no production publication or navigation change. Vercel Git deployment is explicitly disabled for `feature/mind-announcement` in this branch, using the documented per-branch configuration: https://vercel.com/docs/project-configuration/git-configuration . The PR must remain unmerged until publication is authorized.

## Preview

From repository root:

```sh
python3 -m http.server 8765 --directory dist
```

Open http://localhost:8765/mind/ . The existing website is plain static HTML/CSS/JavaScript: no build, package install, lint task or TypeScript/typecheck task is configured. The checked-in `dist/mind` route is the build artifact. No framework migration.

## Validation

```sh
python3 -m unittest discover -s tests -p '*.py'
node --check dist/mind/mind.js
node tests/check-film-controls.cjs
git diff --check
```

25 Python checks pass, including 10 announcement checks. Source hashes, exact trace fields, zero scientific updates, all benchmark cells and existing historical assets are checked. Math intervals use saved Wilson values when present, otherwise derive Wilson95 directly from frozen correct/task counts. Physics bars show original scene means, with uncertainty links rather than invented error bars.

Browser QA: Markov/recurrent switch; all four domain trace options; original prediction / intermediate state / output / verification; next state; arrow-key tab navigation; mathematical seed/family filters; physical family/horizon/metric filters; animation pause; 390px mobile no horizontal page overflow. No browser console errors. Desktop and mobile screenshots included. Animation stops for reduced motion and hidden documents; textual architecture and evidence links remain without JavaScript. No automated screen-reader certification is claimed.

## Evidence

Model source repository: https://github.com/akilanpl/mindscape . Pinned commit `950a17519f43fbc887e41f29ce2e24d4b6036ead` contains the latest R5.4 Alpha readiness supplement. Exact 14 exports live in `dist/mind/evidence`, with source paths, commit URLs and SHA256 in `manifest.json`. `release-r5.4.json` is the presentation bundle; tests compare all displayed trace and benchmark data with exported originals.

R5.4 engineering qualification is verified. Science is UNRUN, zero scientific updates and zero neural OOD predictions. 144 disposable engineering optimizer steps are not learning fits. No R5.4 outputs are invented. All four displayed executions are historical V3 demonstrations; both mathematical failures are retained. R5.2/R5.3 are independently reviewed post-hoc recoveries of failed original campaigns, not clean successful campaigns. Repeated seeds are not extra independent tasks. No research code, frozen artifact, checkpoint, sealed set or tag was modified. No neural execution or new media generation.

The visual reference is https://openai.com/index/gpt-6-astra/ : cinematic dark particle introduction, editorial narrative and interactive evidence. This implementation uses original Mindscape graphics/content and existing site fonts; it copies no OpenAI media or scientific claims.

## Future versions

Keep prior evidence bundles immutable. Add a new release JSON following `mindscape.announcement/1`, export and hash its independent evidence, and point the page's `data-release` attribute to it. Set the reviewed status in `data-status` and update editorial text/status-specific validation. Models, timeline entries, recordings and benchmark rows are versioned data. A trained release must update the deliberate zero-update guard and associated evidence tests; it cannot silently replace this unrun preview. No layout redesign is required.

To reproduce this release export from a checkout containing the pinned commit:

```sh
python3 scripts/export_mind_evidence.py --research /absolute/path/to/mindscape
```

This only reads Git objects and writes website exports. It runs no research experiment.

## Architecture diagram follow-up

The user reported the existing three-step methods diagram collapsing in the middle. Its CSS retained five tracks from a prior arrows layout. The targeted architecture.css correction uses three equal minmax columns and aligned heading height, retaining the one-column mobile breakpoint. Browser measurements: three 277.33px tracks at 1440px, three 213px tracks at 960px, three vertically stacked 294px cards at 390px; no step overflow. Two repair screenshots are included. This is the only intentional change to an existing dist file; the other 189 existing production files remain byte-identical. Publication remains deferred pending review.
