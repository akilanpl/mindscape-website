# Mindscape website

Mindscape’s complete static research website: cinematic home, About, research overview/index/reports, Advancements, Architecture, Safety Overview, Deployment Safety, Resources, and Contact.

## Local preview

Run `python3 -m http.server 4173 --directory dist` and open http://localhost:4173/. No dependencies or build step are required. HTML, CSS, JavaScript, fonts, videos, research documents, data, and figures are all included in `dist/`.

## Vercel

Import this GitHub repository into Vercel. Framework: Other. Root directory: repository root. Output directory: `dist`. No build command. The checked-in `vercel.json` configures static hosting and trailing slash routes. Pushes to `main` should deploy through Vercel’s Git integration.

## Contact form

The two-step form posts to FormSubmit for akilanpalaniyappan105@gmail.com. A setup submission triggered the activation email; the mailbox owner must activate the form before forwarding works. FormSubmit handles its own post-submission confirmation and spam checks.

## Evidence

Report statements are scoped to the preserved research evidence. Historical validation counts are not new production tests. No deployment security certification is claimed.
