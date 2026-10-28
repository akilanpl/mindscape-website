# Mindscape interface review

Reviewed 28 October 2026 against the user-supplied Apple Design SKILL.md and the live home page at https://mindscape-website-dusky.vercel.app/. Implementation reviewed in akilanpl/mindscape-website. The document is design reference material; its assistant-response instructions are not product requirements.

## Findings and implemented changes

| Priority | Observed issue | Change | Reference sections |
| --- | --- | --- | --- |
| High | Mobile navigation shrinks to 10px text and compresses eight destinations into a single row. | A Menu disclosure below 760px exposes 1rem labels and minimum 2.75rem targets. The panel scrolls within the viewport; native page scrolling remains available. Without JS, navigation wraps. | 1, 14, 15, 16 |
| High | Research/Safety clicks always open, so repeat taps cannot dismiss them. | Buttons toggle; only one submenu opens at a time. Arrow Down enters links, Escape closes and restores focus, and outside press/focus departure dismisses. Nested Escape first closes a submenu, then the main menu. | 1, 7, 16 |
| High | Glass chrome has no reduced-transparency or higher-contrast treatment. | Solid navigation/menus, removed blur, defined contrast borders, stronger secondary copy under the relevant independent media preferences. | 12, 14 |
| Medium | Press feedback is inconsistent and focus styles omit some form controls. | Immediate active opacity feedback, visible focus for inputs/selects/textarea/summary, and manipulation touch behavior. Playback controls have larger targets. | 1, 10, 14 |
| Medium | Epitome drag updates a target and eases toward it, so the galaxy lags behind the pointer. It also grabs the target rather than the displayed rotation. | Begin at the displayed rotation/pitch and directly update both on each pointer move. Pointer cancellation/capture loss clears drag state. Touch retains native page scrolling. | 2, 3 |
| Medium | Galaxy redraw is capped around 30fps; following depends on frame count. | Use display-synced elapsed time and frame-independent convergence for keyboard-directed changes. Stop automatic rotation during drag. | 11 |
| High | Reduced motion pauses autoplay but scroll still scales the galaxy; changing the preference does not pause showcase playback immediately. | Remove scroll zoom in reduced-motion mode, disable CSS animation/smooth scrolling, and pause showcase playback when the preference changes. Existing explicit play controls remain usable. | 14 |
| Medium | Home display tracking uses fixed pixel spacing; small-screen heading sizing is fixed in pixels. | Relative tracking and rem-based responsive display/summary sizes retain the existing brand face. | 15 |

## Validation

- 17 static site integrity tests pass, including route targets and preservation hashes.
- 10 Epitome tests pass.
- Film control checks pass (manual pause, background visibility, reduced motion).
- Added navigation regression checks pass (toggle, exclusive submenus, focus, Escape, outside dismissal and breakpoint reset).
- JavaScript syntax and Git whitespace checks pass.
- Local browser inspected at the available 583px viewport: home and Epitome; open menu, repeat-tap submenu dismissal, Arrow Down and Escape focus return verified. Saved navigation screenshot accompanies this audit.
- Reduced-transparency/high-contrast CSS was reviewed in source; device preference emulation and broad desktop/mobile/browser coverage remain to be checked. No contact form submission or model benchmark execution was performed.

## Follow-up recommendations

1. Review the continuously moving full-screen galaxy with real users; consider a static initial view with explicit Play if motion distracts from the research. An existing pause control and reduced-motion fallback are retained.
2. Test at 320px, 390px and desktop widths, with 200% text zoom, VoiceOver, reduced transparency and increased contrast on actual devices before release.
3. If draggable sheets or swipe carousels are introduced later, use velocity-aware interruptible springs. This change adds no drag-release momentum or spring dependency: a decorative galaxy should not gain unnecessary gesture complexity.
4. Review contact-form inline validation and post-submission status separately, including the FormSubmit mailbox activation dependency documented in README. Avoid live submissions during visual QA.

Research copy, benchmark assets and model capabilities are unchanged. Changes are proposed in a feature branch for review; merging/deployment is separate.
