# Centering Indigenous Ways of Knowing Through Open-Source Research Tools

**Valentín Quiroz de la Sierra, PhD, MSW** · Postdoctoral Fellow, Johns Hopkins Center for Indigenous Health

- **Host:** [Partners for Advancing Health Equity (P4HE)](https://www.partners4healthequity.org), Tulane University, with support from the Robert Wood Johnson Foundation
- **Date:** Thursday, November 19, 2026, 12:30–1:30 PM PST
- **Format:** online workshop ([event page](https://www.eventbrite.com/e/centering-indigenous-ways-of-knowing-through-open-source-research-tools-tickets-2003314778430))
- **Recording:** to be posted on the P4HE website

## About the workshop

The workshop introduced Choachoakte Software (Sticky Software), now called MalverdeSoftware, which builds free, open-source research tools grounded in Indigenous Ways of Knowing. It explored how Indigenous Ways of Knowing can shape community-based participatory research and the tools that support it.

The session had four parts:

1. **Watch:** why Indigenous-led software matters, with examples from the Indigenous Wholistic Factors Project and its work with Native youth.
2. **Pitch in:** attendees voted in [mVote](https://mvote.app) on the factors that matter most for youth wellbeing.
3. **Build together:** their votes went straight into a machine learning model (LASSO), run live in a notebook.
4. **Reflect:** a closing discussion using the Belmont Process (See, Hear, Feel), named for Harold Belmont (Suquamish Tribe).

## Results

Attendees placed 207 dots across 25 plain-language factors, and every factor received at least one vote. Hope for the future received the most, with 18. The model kept 14 factors. Six were higher risk (feeling sad or down, feeling hopeless, feeling lonely, being bullied, violence at school, and worry and nerves), six were protective (hope for the future, family support, belonging at school, handling big feelings, feeling safe at home, and friends who have your back), and two were weak or unstable. Its cross-validated AUC was 0.89 (95% interval 0.87 to 0.91), close to the 0.87 of the published model on real data.

These results come from synthetic data and show how the method works. Some of the most popular factors, such as getting enough sleep and unstable housing, dropped out because they carried little signal in the simulated data or overlapped with factors the model kept. Their absence says nothing about their importance in young people's lives.

## Files

- [`run/P4HE_live_vote_demo_nov19-2026_run.ipynb`](run/P4HE_live_vote_demo_nov19-2026_run.ipynb): the saved notebook, with every chart and table
- [`run/nov19_p4he_votes.csv`](run/nov19_p4he_votes.csv): vote totals for each factor
- [`run/nov19_p4he_model_results.csv`](run/nov19_p4he_model_results.csv): the model results

To rerun the session, open the shorter notebook in [`live_vote_demo/`](../../live_vote_demo/README.md) and set `RESULTS_CSV` to the vote totals file.

## Tools shown

- [mVote](https://mvote.app): sticky-dot voting with no accounts or names
- [mPile](https://mpile.app): card sorting for community activities
- Source code: [github.com/MalverdeSoftware](https://github.com/MalverdeSoftware) (Apache-2.0)

## Background

The demonstration follows the published IWFP analysis (Sierra, 2026, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)).
