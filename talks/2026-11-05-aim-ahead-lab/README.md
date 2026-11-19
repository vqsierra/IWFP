# Research Talk and Discussion · Hands-on AI Lab Session

**Valentín Quiroz de la Sierra, PhD, MSW** · Postdoctoral Fellow, Johns Hopkins Center for Indigenous Health

- **Event:** AIM-AHEAD AIHEC AI Master and Catalyze (AMC) Program, in-person workshop, November 4–5, 2026
- **Host:** Centers for American Indian and Alaska Native Health, University of Colorado Anschutz Medical Campus, Aurora, CO
- **Date:** Thursday, November 5, 2026. The agenda placed the talk on Day 1 (Nov 4), and it moved to Day 2 to fit the flow of the workshop. The vote board kept the name `nov4-talk`.
- **Format:** in person
- **Recording:** not recorded

## About the session

The session had two parts for AMC awardees:

1. **Research talk and discussion:** an overview of the Indigenous Computational Approach, told through an accessible metaphor, followed by questions.
2. **Hands-on AI lab:** a participatory feature-selection activity. Candidate features were posted around the room, participants voted as a group in [mVote](https://mvote.app), and the votes were tallied and run live in a notebook to show how the group's choices shape the results.

## Live demonstration

The demo ran live with the room using the board `nov4-talk` (84 items, with the outcome `si` left off). The session's official record is in [MalverdeSoftware/mvote, `demos/nov4-iwfp-talk/`](https://github.com/MalverdeSoftware/mvote/tree/main/demos/nov4-iwfp-talk).

- **Votes:** 13 participant records, 177 dots, 75 of the 84 items got at least one dot (most dots on one item: 6). Totals are in [`nov5_lab_votes.csv`](run/nov5_lab_votes.csv). This repo holds only per-item totals. The board itself also keeps one record per participant, with that person's votes and remaining dots, and those records are not published here.
- **Model:** 55 voted items entered the LASSO. Seven were kept as higher risk (depressive symptoms, other psychological distress, loneliness, feeling hopeless, trauma-related symptoms, bullying, self-harm), five as protective (emotion regulation, positive emotional wellbeing, family support, optimism, life satisfaction), and four were weak or unstable. The other 39 were dropped. The table is in [`nov5_lab_model_results.csv`](run/nov5_lab_model_results.csv).
- **Reading it:** these are synthetic-data results, so they show how the method treats the room's choices, not what predicts ideation among Native youth. Correlated items compete (anxiety was dropped while depressive symptoms, distress and hopelessness were kept), which is why the dropped list is not a list of unimportant factors.

## Files

- [`run/IWFP_live_vote_demo_nov5-2026_run.ipynb`](run/IWFP_live_vote_demo_nov5-2026_run.ipynb): the saved notebook run, with every chart and table. To run it again, use the blank notebook in [`live_vote_demo/`](../../live_vote_demo/) with `RESULTS_CSV` set to the vote totals below.
- [`run/nov5_lab_votes.csv`](run/nov5_lab_votes.csv): the room's dot totals
- [`run/nov5_lab_model_results.csv`](run/nov5_lab_model_results.csv): the model's result table

## Background

The model follows the published Indigenous Wholistic Factors analysis: Sierra (2026), [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/).
