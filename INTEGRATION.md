# Integration: Simulation Engine → worldcup-pwa

## Overview

The simulation engine (`worldcup-sim/`) generates a `scenarios.json` file that serves as the data backbone for the worldcup-pwa bracket view. This file is automatically regenerated every 6 hours via GitHub Actions as group stage results are finalized.

## Architecture

```
worldcup-sim/                           standalone repo
├── mock_data.py                        (group stage results)
├── group_stage.py                      (calculate standings)
├── bracket_mapper.py                   (map to R32)
├── export_scenarios.py                 (generate JSON)
└── scenarios.json                      (output)
        │
        ├────────────────────────────────────────────────────┐
        │                                                     │
   .github/workflows/                                  worldcup-app/
   generate-scenarios.yml               packages/data/src/
   (GitHub Actions trigger)             scenarios-loader.ts
        │                               (consume JSON in browser)
        └──► Commit scenarios.json to worldcup-app repo
             (via automated PR)
```

## Format: scenarios.json

Each R32 match contains possible team pairings with probabilities:

```json
{
  "generated_at": "2026-06-24T20:07:10.635585Z",
  "version": "1.0",
  "r32_matches": [
    {
      "match": 1,
      "team1_options": [
        {
          "team": "USA",
          "group": "A",
          "slot": "W1",
          "probability": 1.0
        }
      ],
      "team2_options": [
        {
          "team": "Brazil",
          "group": "B",
          "slot": "R2",
          "probability": 1.0
        }
      ]
    }
  ]
}
```

**Current State (Mock Data):**
- All probabilities are 1.0 (deterministic)
- One definite matchup per R32 slot

**Phase 2 (Probabilistic Simulations):**
- Run N tournament simulations with random outcomes
- For each R32 match, show all possible team pairings and their % likelihood
- Example:
  ```json
  "team1_options": [
    { "team": "USA", "group": "A", "probability": 0.75 },
    { "team": "Canada", "group": "A", "probability": 0.25 }
  ]
  ```

## TypeScript Consumer API

The `scenarios-loader.ts` module in worldcup-app provides helpers:

```typescript
import {
  loadScenarios,
  getMostLikelyMatchup,
  getPossibleOutcomes,
  getMatchConfidence,
  formatMatchupDisplay,
} from "@worldcup-app/data";

// Load scenarios
const scenarios = await loadScenarios("/data/scenarios/latest.json");

// For Match 1:
const match1 = scenarios.r32_matches[0];

// Get most likely teams
const outcome = getMostLikelyMatchup(match1);
// { team1: "USA", team2: "Brazil" }

// Get all possible outcomes with probabilities
const outcomes = getPossibleOutcomes(match1);
// [
//   { team1: "USA", team2: "Brazil", probability: 1.0 },
//   ...
// ]

// Get confidence (0-1)
const confidence = getMatchConfidence(match1); // 1.0 = certain

// Format for display
const display = formatMatchupDisplay(match1);
// "USA vs Brazil" or "USA vs Brazil (75%)" if uncertain
```

## GitHub Actions Workflow

**File:** `.github/workflows/generate-scenarios.yml`

**Required CI config in `worldcup-sim` repo:**
- Repository variable: `WORLDCUP_APP_REPO` (format: `owner/worldcup-app`)
- Repository secret: `WORLDCUP_APP_TOKEN` (PAT with contents + pull request write access to `worldcup-app`)

**Triggers:**
1. **Schedule**: Every 6 hours (cron)
2. **Manual**: Via workflow_dispatch
3. **On Change**: When `mock_data.py` or workflow itself changes

**Steps:**
1. Checkout worldcup-sim repo
2. Run `python export_scenarios.py` → `worldcup-sim/scenarios.json`
3. Copy to `worldcup-app/packages/data/data/scenarios/latest.json`
4. Create automated PR to worldcup-app with updated scenarios

## Integration Checklist

- [x] Python engine generates `scenarios.json`
- [x] GitHub Actions workflow configured
- [x] TypeScript loader module created
- [ ] Deploy to worldcup-app repo
- [ ] Wire up bracket UI component to use scenarios-loader
- [ ] Add confidence/probability visualization to bracket

## Next Steps

### Phase 2: Probabilistic Simulation
1. Add `--num-simulations N` flag to export_scenarios.py
2. Run N random tournament outcomes with team strength ratings
3. Aggregate results: for each R32 slot, calculate % of simulations where each team qualified
4. Export per-match probabilities to scenarios.json

Example:
```bash
python export_scenarios.py --num-simulations 10000 --team-ratings ratings.csv
```

### Phase 3: Live Updates
1. Integrate with real FIFA API / ESPN for live group stage scores
2. Update scenarios.json as matches complete (continuous rather than every 6 hours)
3. Add match replay / live match tracking to scenarios

### UI Integration
1. Show confidence indicators in bracket (color, opacity, badge)
2. Hover on match → show all possible outcomes + probabilities
3. "What if..." mode: simulate different group outcomes
