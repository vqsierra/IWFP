# Research Talk and Discussion · Hands-on AI Lab Session

**Valentín Quiroz de la Sierra, PhD, MSW** · Postdoctoral Fellow, Johns Hopkins Center for Indigenous Health

- **Event:** AIM-AHEAD AIHEC AI Master and Catalyze (AMC) Program, in-person workshop, November 4–5, 2026
- **Host:** Centers for American Indian and Alaska Native Health, University of Colorado Anschutz Medical Campus, Aurora, CO
- **Date:** Thursday, November 5, 2026
- **Format:** in person
- **Recording:** not recorded

## About the session

The session for AMC awardees had two parts:

1. **Research talk and discussion:** an overview of the Indigenous Computational Approach, told through an accessible metaphor, followed by questions.
2. **Hands-on AI lab:** a group feature-selection activity. Candidate factors were posted around the room, and participants voted on them in [mVote](https://mvote.app). The votes were then run live in a notebook to show how the group's choices shape a model.

## Results

Thirteen participants placed 177 dots, and 75 of the 84 factors received at least one vote. The 55 factors chosen by the group went into the model. It kept seven as higher risk (depressive symptoms, other psychological distress, loneliness, feeling hopeless, trauma-related symptoms, bullying and self-harm) and five as protective (emotion regulation, positive emotional wellbeing, family support, optimism and life satisfaction). Four were weak or unstable, and the model set the remaining 39 aside.

These results come from synthetic data, so they show how the method treats a group's choices and say nothing about what predicts suicidal ideation among Native youth. Closely related factors compete with each other in this kind of model. Anxiety, for example, was set aside because depressive symptoms, distress and hopelessness carried overlapping information, so a factor the model leaves out can still matter.

## Files

- [`run/IWFP_live_vote_demo_nov5-2026_run.ipynb`](run/IWFP_live_vote_demo_nov5-2026_run.ipynb): the saved notebook, with every chart and table
- [`run/nov5_lab_votes.csv`](run/nov5_lab_votes.csv): vote totals for each factor
- [`run/nov5_lab_model_results.csv`](run/nov5_lab_model_results.csv): the model results

To rerun the session, open the full notebook in [`live_vote_demo/`](../../live_vote_demo/README.md) and set `RESULTS_CSV` to the vote totals file.

## Background

The demonstration follows the published IWFP analysis (Sierra, 2026, [PMC12424082](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424082/)). mVote is part of [MalverdeSoftware](https://github.com/MalverdeSoftware), a set of free, open-source research tools.
