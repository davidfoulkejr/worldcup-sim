# World Cup Simulation Engine ↔ worldcup-pwa Integration Guide

## Summary

The simulation engine is **fully integrated** with worldcup-pwa. Here's the complete pipeline:

```
INPUT                PROCESSING              OUTPUT                  UI CONSUMPTION
──────                ──────────              ──────                  ──────────────

Group Stage    ───→  Group Stage      ───→  Bracket      ───→  scenarios.json  ───→  worldcup-pwa
Results              Standings              Mapping                                    Bracket View
(mock_data.py)       (2026 rules)           (R32 slots)            (every 6h via
                                                                    GitHub Actions)
```

## Files Created

### Simulation Engine (worldcup-sim repo)

1. **`export_scenarios.py`**
   - Generates `scenarios.json` from group standings
   - Per-match team options with probabilities
   - Ready for Phase 2 probabilistic simulations

2. **`scenarios.json`** (generated)
   - 16 R32 matches with possible pairings
   - Currently deterministic (all probabilities 1.0)
   - Format: `{ match, team1_options[], team2_options[] }`

3. **`.github/workflows/generate-scenarios.yml`**
   - Automated regeneration every 6 hours
   - Triggers on `mock_data.py` changes or manual dispatch
   - Creates PR to worldcup-app with updated scenarios

### Web App Integration (worldcup-app repo)

1. **`packages/data/src/scenarios-loader.ts`**
   - TypeScript consumer module
   - Helper functions: `loadScenarios()`, `getMostLikelyMatchup()`, `getPossibleOutcomes()`, etc.
   - Handles confidence calculations and display formatting

## Data Flow

### Current (Mock Data - Deterministic)

```
Match 1:
├── team1_options: [ { team: "USA", group: "A", probability: 1.0 } ]
└── team2_options: [ { team: "Brazil", group: "B", probability: 1.0 } ]

Result: USA vs Brazil (100% certain)
```

### Phase 2 (Probabilistic - After 10,000 Simulations)

```
Match 1:
├── team1_options:
│   ├── { team: "USA", group: "A", probability: 0.95 }
│   └── { team: "Canada", group: "A", probability: 0.05 }
└── team2_options:
    ├── { team: "Brazil", group: "B", probability: 0.92 }
    └── { team: "Mexico", group: "A", probability: 0.08 }

Results:
├── USA vs Brazil: 87.4% likely
├── USA vs Mexico: 7.6% likely
├── Canada vs Brazil: 4.6% likely
└── Canada vs Mexico: 0.4% likely
```

## Usage in worldcup-pwa

### Load scenarios in a React component:

```typescript
import { loadScenarios, formatMatchupDisplay } from "@worldcup-app/data";

export function R32Match({ matchNumber }) {
  const [scenarios, setScenarios] = useState(null);

  useEffect(() => {
    loadScenarios().then(setScenarios);
  }, []);

  if (!scenarios) return <div>Loading...</div>;

  const match = scenarios.r32_matches[matchNumber - 1];
  const display = formatMatchupDisplay(match);
  const confidence = getMatchConfidence(match);

  return (
    <div className={`match ${confidence < 1 ? "uncertain" : "confirmed"}`}>
      <h3>Match {matchNumber}</h3>
      <p>{display}</p>
      {confidence < 1 && <span className="confidence">{Math.round(confidence * 100)}%</span>}
    </div>
  );
}
```

### Or access raw scenarios:

```typescript
const scenarios = await loadScenarios("/data/scenarios/latest.json");
const match1 = scenarios.r32_matches[0]; // Match 1

// Get all possible outcomes
const outcomes = getPossibleOutcomes(match1);
outcomes.forEach(({ team1, team2, probability }) => {
  console.log(`${team1} vs ${team2}: ${(probability * 100).toFixed(1)}%`);
});
```

## GitHub Actions Workflow

**Location:** `.github/workflows/generate-scenarios.yml`

**Triggered by:**
- ✓ Schedule: Every 6 hours (even during tournament)
- ✓ Manual: Via workflow_dispatch button
- ✓ Code change: When `mock_data.py` or workflow file changes

**Creates:**
- Automated PR to worldcup-app updating scenarios

## Deployment Steps

### 1. Run in worldcup-sim repo
```bash
cd worldcup-sim
python export_scenarios.py  # generates scenarios.json
```

### 2. Deploy to worldcup-app repo
```bash
# Copy scenarios-loader.ts to packages/data/src/
# Create data/scenarios/ directory
# Add latest.json endpoint or static file serving
```

### 3. Update worldcup-app package.json (export)
```json
{
  "exports": {
    "./scenarios-loader": "./src/scenarios-loader.ts"
  }
}
```

### 4. Wire up bracket view
```typescript
import { loadScenarios, formatMatchupDisplay } from "@worldcup-app/data";
// Use in your bracket component
```

## Testing

### Verify scenarios.json generation:
```bash
cd worldcup-sim
python export_scenarios.py
cat scenarios.json | jq '.r32_matches[0]'
```

### Test scenarios-loader in browser:
```typescript
import { loadScenarios, getPossibleOutcomes } from "@worldcup-app/data";

const scenarios = await loadScenarios("/data/scenarios/latest.json");
const match1 = scenarios.r32_matches[0];
console.log(getPossibleOutcomes(match1));
```

## Next Steps

### Phase 2: Probabilistic Simulations
1. Add team strength ratings (ELO, FIFA ranking, etc.)
2. Run Monte Carlo simulations (N random tournaments)
3. Calculate per-match probabilities
4. Command:
   ```bash
   python export_scenarios.py --simulations 10000 --ratings fifa-rankings.csv
   ```

### Phase 3: Live Integration
1. Fetch real group stage results from FIFA API
2. Update scenarios continuously (not just every 6h)
3. Track live match events

### UI Enhancements
1. Confidence badges (color/opacity based on probability)
2. Hover → show all possible outcomes
3. "What if" simulator (manual team selection)
4. Historical accuracy tracking (did Phase 1 predictions match Phase 2 outcomes?)

## Architecture Summary

```
Input                 Python Engine           Output           TypeScript/React
─────                 ─────────────           ──────           ────────────────

mock_data.py    ─→ group_stage.py       ─→ scenarios.json ──→ scenarios-loader.ts
(12 groups)     ─→ bracket_mapper.py    ─→ (16 R32 matches)   (browser consumer)
                ─→ export_scenarios.py
                
                      ↓ (GitHub Actions)
                      
              .github/workflows/generate-scenarios.yml
              
              ↓ Commits to worldcup-app repo
              
          packages/data/data/scenarios/latest.json
          (serves in worldcup-pwa bracket view)
```

## Questions?

See `INTEGRATION.md` for detailed format specs and `README.md` for engine capabilities.
