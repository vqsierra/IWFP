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

The highlights notebook ran live on the board `p4he-nov19` (25 plain-language factors). The saved run is [`P4HE_live_vote_demo_nov19-2026_run.ipynb`](run/P4HE_live_vote_demo_nov19-2026_run.ipynb).

- **Votes:** 207 dots, and all 25 factors got at least one (most dots: Hope for the future, 18). Totals are in [`nov19_p4he_votes.csv`](run/nov19_p4he_votes.csv). As with the Nov 5 run, only per-item totals are published here.
- **Model:** the LASSO kept 14 of the 25 factors. Six were higher risk (feeling sad or down, feeling hopeless, feeling lonely, being bullied, violence at school, worry and nerves), six protective (hope for the future, family support, belonging at school, handling big feelings, feeling safe at home, friends who have your back), and two weak or unstable. The other 11 were dropped. Cross-validated AUC was 0.89 (0.87 to 0.91), against 0.87 for the published model on real data. The table is in [`nov19_p4he_model_results.csv`](run/nov19_p4he_model_results.csv).
- **Reading it:** these are synthetic-data results. Some of the room's most-voted factors (getting enough sleep, unstable housing) were dropped because they carry little signal in the simulated data or overlap with kept factors. The drop says nothing about their real importance.

The session record and board are in [MalverdeSoftware/mvote, `demos/nov19-p4he-workshop/`](https://github.com/MalverdeSoftware/mvote/tree/main/demos/nov19-p4he-workshop). To run the notebook again, use the blank highlights notebook in [`live_vote_demo/`](../../live_vote_demo/) with `RESULTS_CSV` set to the vote totals.

## Tools shown

- [mVote](https://mvote.app): sticky-dot voting with no accounts or names
- [mPile](https://mpile.app): card sorting for community activities
- Code: [github.com/MalverdeSoftware](https://github.com/MalverdeSoftware) (Apache-2.0)

## Background

The model follows the published Indigenous Wholistic Factors analysis: Sierra (2026), [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/).

Slides are not posted.
