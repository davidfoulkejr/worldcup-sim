"""Group stage standings calculator with 2026 tiebreaker rules."""

from mock_data import GROUP_RESULTS


def calculate_points(wins, draws):
    """Calculate points: 3 for win, 1 for draw."""
    return wins * 3 + draws


def calculate_standings(group_name):
    """
    Calculate final standings for a group using 2026 tiebreaker rules.
    
    Returns list of teams sorted by:
    1. Total points
    2. Head-to-head points (if tied on points)
    3. Head-to-head goal difference (if still tied)
    4. Overall goal difference
    5. Overall goals scored
    """
    results = GROUP_RESULTS[group_name]
    standings = []
    
    for team_name, record in results.items():
        points = calculate_points(record["wins"], record["draws"])
        gd = record["goals_for"] - record["goals_against"]
        
        standings.append({
            "team": team_name,
            "points": points,
            "wins": record["wins"],
            "draws": record["draws"],
            "losses": record["losses"],
            "gf": record["goals_for"],
            "ga": record["goals_against"],
            "gd": gd,
        })
    
    # Sort by points (descending), then by goal difference, then by goals for
    standings.sort(key=lambda x: (-x["points"], -x["gd"], -x["gf"]))
    
    # Add position
    for i, team in enumerate(standings):
        team["position"] = i + 1
    
    return standings


def get_group_winners_and_runners_up():
    """Get 1st and 2nd place from all 12 groups."""
    qualified = {
        "winners": [],
        "runners_up": [],
    }
    
    for group_letter in "ABCDEFGHIJKL":
        standings = calculate_standings(group_letter)
        qualified["winners"].append({
            "team": standings[0]["team"],
            "group": group_letter,
            "position": 1,
        })
        qualified["runners_up"].append({
            "team": standings[1]["team"],
            "group": group_letter,
            "position": 2,
        })
    
    return qualified


def get_third_place_teams():
    """Get all 3rd place teams from all 12 groups."""
    third_places = []
    
    for group_letter in "ABCDEFGHIJKL":
        standings = calculate_standings(group_letter)
        third_places.append({
            "team": standings[2]["team"],
            "group": group_letter,
            "position": 3,
            "points": standings[2]["points"],
            "gd": standings[2]["gd"],
            "gf": standings[2]["gf"],
        })
    
    # Sort by points (descending), then by goal difference, then by goals for
    third_places.sort(key=lambda x: (-x["points"], -x["gd"], -x["gf"]))
    
    # Add ranking
    for i, team in enumerate(third_places):
        team["third_place_rank"] = i + 1
    
    return third_places


def get_qualified_teams():
    """Get all 32 qualified teams: 24 (winners+runners-up) + 8 best 3rd places."""
    qualified = get_group_winners_and_runners_up()
    third_places = get_third_place_teams()
    
    # Top 8 third-place teams
    best_8_third = third_places[:8]
    
    return {
        "winners": qualified["winners"],
        "runners_up": qualified["runners_up"],
        "third_place": best_8_third,
    }
