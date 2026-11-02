# Neil Fox Agency GitHub profile design

## Reference and capture context

- Reference site: https://neilfoxagency.com/
- Visual reference: user-supplied homepage screenshot, “Screenshot 2026-11-02 at 5.17.49 AM.png,” inspected for layout and color. Live page text and branding metadata were retrieved 2026-11-02; a full-page 1440 × 1100 desktop capture was requested.
- Profile content: https://github.com/NeilFoxAgency/NeilFoxAgency/blob/main/README.md (public self-description and links).
- Exact local site tokens: ../NeilFoxAgency/client/src/index.css; font declarations: ../NeilFoxAgency/client/index.html.
- Logo source: https://neilfoxagency.com/brand/neil-fox-logo.webp; a copy is included at assets/neil-fox-logo.webp for the banner renderer.

The captured hero uses a deep ink background, a restrained blue edge around a campaign dashboard, orange emphasis, and a large display-serif headline. The profile adapts those cues to GitHub's single-column README rather than trying to reproduce the website navigation or page layout.

## Design tokens

| Role | Value | Evidence / use |
| --- | --- | --- |
| Ink | #031022 | Site CSS --ink; banner canvas |
| Ink secondary | #07172C | Site CSS --ink-2; inset panels |
| Panel | #0B1B31 | Site CSS --panel; workflow card |
| Agency chrome | #202B3A | Website header visible in supplied screenshot |
| Orange | #FF4D12 | Site CSS --orange; primary accent and moving signal |
| Orange highlight | #FF6A24 | Site CSS --orange-2; warm gradient accents |
| Electric blue | #47A8FF | Site CSS --blue; panel outlines and process path |
| Mint | #31D6A0 | Site CSS --mint; secondary status detail |
| Warm white | #FFFEFA | Site CSS --white; display and body text |
| Muted copy | #667085 | Site CSS --muted; supporting copy |

Typography follows the site: DM Serif Display for the wordmark and headline, DM Sans for body copy, labels, and interface text. The matching TrueType fonts and OFL notices are bundled under assets/fonts so the banner can be regenerated consistently.

## Layout and components

1. Full-width animated hero image at the beginning of the profile README.
2. Compact contact/navigation row linking to the agency, creator page, brand page, email, X, and LinkedIn.
3. Concise founder/agency introduction and three profile-stated milestones.
4. Short sections for developer creators, dev-tool/SaaS teams, and selected public projects.
5. Contact and location line at the end.

The banner has a slim brand bar with the original fox mark, a two-line serif headline and short agency description on the left, and a blue-edged workflow panel on the right. The process panel covers creator fit, coordination/creative control, and a useful recap. An orange signal travels slowly between those steps; a soft halo follows it. The loop is intentionally restrained, with no flashing or rapid motion.

The site screenshot's sample dashboard includes explicitly illustrative campaign sales and ROAS values. Those numbers are not reused. The README instead includes milestones already stated in the public profile: 70K+ subscribers, 17M+ views, and $1M+ ArtworkTee lifetime revenue. They remain profile-stated claims, not independently verified results.

## Assets and regeneration

- assets/profile-banner.gif is the looping image embedded by README.md.
- assets/profile-banner-preview.png is the still frame for quick inspection or use where animation is unwanted.
- scripts/render_profile_banner.py draws both from the copied logo and bundled fonts using Pillow.
- Regenerate with Python 3 and Pillow: python3 -m pip install Pillow, then python3 scripts/render_profile_banner.py.

The GIF is a self-contained visual loop; it does not claim to show live campaign results and does not need a scheduled GitHub Action. Repository/project links and profile copy remain ordinary Markdown for readability and accessibility.

## Unresolved details

- The animation is a static looping asset, not a live data feed. No external stats service, private API, GitHub token, or workflow permission is required.
- GitHub's responsive rendering and image cache can differ from a local preview; final sizing should be checked on the live profile after the user publishes the repository changes.
