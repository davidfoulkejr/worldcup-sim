"""Mock 2026 FIFA World Cup data for testing."""

# 12 groups of 4 teams each
GROUPS = {
    "A": [
        {"name": "USA", "strength": 85},
        {"name": "Mexico", "strength": 82},
        {"name": "Canada", "strength": 78},
        {"name": "Costa Rica", "strength": 72},
    ],
    "B": [
        {"name": "Argentina", "strength": 90},
        {"name": "Brazil", "strength": 88},
        {"name": "Paraguay", "strength": 76},
        {"name": "Bolivia", "strength": 68},
    ],
    "C": [
        {"name": "England", "strength": 86},
        {"name": "France", "strength": 87},
        {"name": "Netherlands", "strength": 84},
        {"name": "Poland", "strength": 75},
    ],
    "D": [
        {"name": "Spain", "strength": 85},
        {"name": "Germany", "strength": 84},
        {"name": "Portugal", "strength": 82},
        {"name": "Serbia", "strength": 74},
    ],
    "E": [
        {"name": "Belgium", "strength": 83},
        {"name": "Italy", "strength": 81},
        {"name": "Austria", "strength": 78},
        {"name": "Albania", "strength": 70},
    ],
    "F": [
        {"name": "Japan", "strength": 80},
        {"name": "South Korea", "strength": 79},
        {"name": "Australia", "strength": 76},
        {"name": "Bahrain", "strength": 68},
    ],
    "G": [
        {"name": "Nigeria", "strength": 77},
        {"name": "Egypt", "strength": 75},
        {"name": "Cameroon", "strength": 74},
        {"name": "Ghana", "strength": 71},
    ],
    "H": [
        {"name": "Morocco", "strength": 78},
        {"name": "South Africa", "strength": 76},
        {"name": "Senegal", "strength": 74},
        {"name": "Tunisia", "strength": 70},
    ],
    "I": [
        {"name": "Uruguay", "strength": 82},
        {"name": "Colombia", "strength": 81},
        {"name": "Ecuador", "strength": 75},
        {"name": "Peru", "strength": 72},
    ],
    "J": [
        {"name": "Chile", "strength": 78},
        {"name": "Venezuela", "strength": 72},
        {"name": "Jamaica", "strength": 68},
        {"name": "Panama", "strength": 65},
    ],
    "K": [
        {"name": "Iran", "strength": 72},
        {"name": "Saudi Arabia", "strength": 70},
        {"name": "UAE", "strength": 68},
        {"name": "Uzbekistan", "strength": 67},
    ],
    "L": [
        {"name": "Switzerland", "strength": 82},
        {"name": "Sweden", "strength": 79},
        {"name": "Norway", "strength": 77},
        {"name": "Wales", "strength": 75},
    ],
}

# Sample group stage results (wins/draws/losses per team in each group)
# Format: {"wins": int, "draws": int, "losses": int, "goals_for": int, "goals_against": int}
GROUP_RESULTS = {
    "A": {
        "USA": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 6, "goals_against": 2},
        "Mexico": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 5, "goals_against": 3},
        "Canada": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 3, "goals_against": 5},
        "Costa Rica": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 1, "goals_against": 5},
    },
    "B": {
        "Argentina": {"wins": 3, "draws": 0, "losses": 0, "goals_for": 8, "goals_against": 1},
        "Brazil": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 7, "goals_against": 2},
        "Paraguay": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 2, "goals_against": 5},
        "Bolivia": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 0, "goals_against": 9},
    },
    "C": {
        "England": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 6, "goals_against": 2},
        "France": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 7, "goals_against": 3},
        "Netherlands": {"wins": 1, "draws": 2, "losses": 0, "goals_for": 4, "goals_against": 2},
        "Poland": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 1, "goals_against": 5},
    },
    "D": {
        "Spain": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 5, "goals_against": 1},
        "Germany": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 6, "goals_against": 2},
        "Portugal": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 4, "goals_against": 3},
        "Serbia": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 2, "goals_against": 7},
    },
    "E": {
        "Belgium": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 6, "goals_against": 2},
        "Italy": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 5, "goals_against": 2},
        "Austria": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 3},
        "Albania": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 0, "goals_against": 7},
    },
    "F": {
        "Japan": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 5, "goals_against": 2},
        "South Korea": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 4, "goals_against": 4},
        "Australia": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 3},
        "Bahrain": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 1, "goals_against": 4},
    },
    "G": {
        "Nigeria": {"wins": 1, "draws": 2, "losses": 0, "goals_for": 4, "goals_against": 2},
        "Egypt": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 2},
        "Cameroon": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 3},
        "Ghana": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 1, "goals_against": 4},
    },
    "H": {
        "Morocco": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 5, "goals_against": 1},
        "South Africa": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 4, "goals_against": 2},
        "Senegal": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 3, "goals_against": 4},
        "Tunisia": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 1, "goals_against": 6},
    },
    "I": {
        "Uruguay": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 6, "goals_against": 2},
        "Colombia": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 5, "goals_against": 2},
        "Ecuador": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 3, "goals_against": 4},
        "Peru": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 2, "goals_against": 5},
    },
    "J": {
        "Chile": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 5, "goals_against": 2},
        "Venezuela": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 3},
        "Jamaica": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 2, "goals_against": 3},
        "Panama": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 1, "goals_against": 3},
    },
    "K": {
        "Iran": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 5, "goals_against": 2},
        "Saudi Arabia": {"wins": 1, "draws": 1, "losses": 1, "goals_for": 3, "goals_against": 3},
        "UAE": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 2, "goals_against": 3},
        "Uzbekistan": {"wins": 0, "draws": 0, "losses": 3, "goals_for": 1, "goals_against": 3},
    },
    "L": {
        "Switzerland": {"wins": 2, "draws": 1, "losses": 0, "goals_for": 5, "goals_against": 1},
        "Sweden": {"wins": 2, "draws": 0, "losses": 1, "goals_for": 4, "goals_against": 2},
        "Norway": {"wins": 1, "draws": 0, "losses": 2, "goals_for": 3, "goals_against": 4},
        "Wales": {"wins": 0, "draws": 1, "losses": 2, "goals_for": 1, "goals_against": 6},
    },
}
