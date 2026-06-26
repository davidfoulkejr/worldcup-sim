# 2026 World Cup Simulation Engine

Generates **Round-of-32 matchup probabilities** (including match numbers like **M84**) using:
- live fixtures/results from `openfootball/worldcup.json`
- live team strengths from `eloratings.net` (World Elo ratings)
- Monte Carlo simulation

## What it outputs

`scenarios.json` with:
- `r32_matches` keyed by official match numbers (`73..88`)
- per-side team probabilities (`team1_options`, `team2_options`)
- full matchup probabilities (`matchup_options`)
- `most_likely_matchup` + confidence

This is the data contract consumed by `worldcup-pwa` Bracket UI.

## Run locally

```bash
python export_scenarios.py --simulations 5000
```

Optional:

```bash
python export_scenarios.py --simulations 10000 --seed 42 --output scenarios.json
```

## Model notes

- Group tables use 2026 ordering: **points → head-to-head points → head-to-head GD → head-to-head GF → overall GD → overall GF**
- Unplayed group matches are simulated from Elo-driven win/draw/loss probabilities.
- Scorelines are sampled from weighted distributions to produce realistic GD/GF for tie-breakers.

## Automation

Workflow: `.github/workflows/generate-scenarios.yml`

- runs every 6 hours
- regenerates `scenarios.json`
- checks out `worldcup-app`
- updates `packages/data/data/scenarios/latest.json`
- opens a PR in `worldcup-app`

Required repo config in `worldcup-sim`:
- variable: `WORLDCUP_APP_REPO` (`owner/worldcup-app`)
- secret: `WORLDCUP_APP_TOKEN` (contents + PR write in `worldcup-app`)
