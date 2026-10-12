# Mindscape website

Mindscape’s complete static research website: cinematic video home, About, research overview/index/reports, Advancements, Architecture, Safety Overview, Deployment Safety, Resources, and Contact.

## Local preview

Run `python3 -m http.server 4173 --directory dist` and open http://localhost:4173/. No dependencies or build step are required. HTML, CSS, JavaScript, fonts, videos, research documents, data, and figures are all included in `dist/`.

## Vercel

Import this GitHub repository into Vercel. Framework: Other. Root directory: repository root. Output directory: `dist`. No build command. The checked-in `vercel.json` configures static hosting and trailing slash routes. Pushes to `main` should deploy through Vercel’s Git integration.

## Contact form

The two-step form posts to FormSubmit for akilanpalaniyappan105@gmail.com. A setup submission triggered the activation email; the mailbox owner must activate the form before forwarding works. FormSubmit handles its own post-submission confirmation and spam checks.

## Evidence

Report statements are scoped to the preserved research evidence. Historical validation counts are not new production tests. No deployment security certification is claimed.

Hero media: nine-second silent writing footage from Pexels, video 33350918 by Kelly (profile @kelly), downloaded October 11, 2026. Source: https://www.pexels.com/video/person-writing-in-notebook-at-desk-33350918/ . License: https://www.pexels.com/license/ (free website use and modification permitted, no endorsement implied). Web encode: 1080×1920 H.264, muted autoplay, loop, no controls. Stock illustration of the research vision, not a Mindscape team member or experiment. Replaces the watermarked OpenArt export.

## V3/V3.1 evidence update — 12 October 2026

All eleven canonical pages include current research scope. The library contains ten new Markdown reports alongside 45 preserved historical PDFs. Current source exports, SHA-256 provenance, native integration traces and replay receipts live in `dist/assets/v3/`; historical assets remain unchanged. Current demonstrations are separated from benchmarks and cross-domain transfer remains unestablished.

Validate with `python3 tests/verify_site.py` and `node --check dist/research.js`. Serve `dist` as above. `scripts/update_v3.py` records the one-time source export/content migration (requires the pinned research checkout); checked-in `dist` is deployable without that checkout or a build step. Subsequent editorial fixes are applied directly to static sources.

The website does not rerun models or expose a research execution endpoint. Contact form behavior remains unchanged; delivery still depends on the mailbox owner's FormSubmit activation. Verification does not send contact submissions.
