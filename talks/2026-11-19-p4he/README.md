# Centering Indigenous Ways of Knowing Through Open-Source Research Tools

**Valentín Quiroz de la Sierra, PhD, MSW** · Postdoctoral Fellow, Johns Hopkins Center for Indigenous Health

- **Host:** [Partners for Advancing Health Equity (P4HE)](https://www.partners4healthequity.org), staffed at Tulane University, with support from the Robert Wood Johnson Foundation
- **Date:** Thursday, November 19, 2026, 12:30 to 1:30 PM PST
- **Format:** online workshop ([event page](https://www.eventbrite.com/e/centering-indigenous-ways-of-knowing-through-open-source-research-tools-tickets-2003314778430))
- **Recording:** P4HE recorded the session and will post it on its website. The link will be added here.

## About the workshop

The workshop introduced Choachoakte Software (Sticky Software, now MalverdeSoftware), an initiative building free, open-source research tools grounded in Indigenous Ways of Knowing. It asked how Indigenous Ways of Knowing can shape community-based participatory research and the tools that support it.

The session had four parts:

1. **Watch:** why Indigenous-led software matters, and earlier work with Native youth on the Indigenous Wholistic Factors Project.
2. **Pitch in:** attendees voted in [mVote](https://mvote.app) on which factors matter most for youth wellbeing.
3. **Build together:** the votes went straight into a machine learning model (LASSO) run live in a notebook.
4. **Reflect:** a closing discussion using the Belmont Process (See, Hear, Feel), named for Harold Belmont (Suquamish Tribe).

## Live demonstration

Attendees placed 207 dots across 25 plain-language factors. The model kept 14 of them, with a cross-validated AUC of 0.89. All modeling used synthetic data, so the results show how the method works. They are not findings about Native youth.

- Saved notebook run, vote totals and results: [`live_vote_demo/`](../../live_vote_demo/) (see the Nov 19 section of its README)
- Session record and board: [MalverdeSoftware/mvote, `demos/nov19-p4he-workshop/`](https://github.com/MalverdeSoftware/mvote/tree/main/demos/nov19-p4he-workshop)

## Tools shown

- [mVote](https://mvote.app): sticky-dot voting with no accounts or names
- [mPile](https://mpile.app): card sorting for community activities
- Code: [github.com/MalverdeSoftware](https://github.com/MalverdeSoftware) (Apache-2.0)

## Background

The model follows the published Indigenous Wholistic Factors analysis: Sierra (2026), [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/).

Slides are not posted.
