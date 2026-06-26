"""Round of 32 bracket mapper."""

from group_stage import get_qualified_teams


# Round of 32 bracket structure
# Maps match slots to potential matchups
# Winners (W1-W12) vs non-winners (R1-R12 or 3rd places)

BRACKET_STRUCTURE = {
    # Match slots are numbered M1-M16 in Round of 32
    # Format: {"slot": "match_number", "team1_slot": "position", "team2_slot": "position"}
    
    # Match 1: W1 vs R2
    1: {"winner_slot": "W1", "non_winner_slot": "R2", "groups": "A/H"},
    # Match 2: W2 vs R1
    2: {"winner_slot": "W2", "non_winner_slot": "R1", "groups": "B/G"},
    # Match 3: W3 vs R4
    3: {"winner_slot": "W3", "non_winner_slot": "R4", "groups": "C/F"},
    # Match 4: W4 vs R3
    4: {"winner_slot": "W4", "non_winner_slot": "R3", "groups": "D/E"},
    # Match 5: W5 vs R6
    5: {"winner_slot": "W5", "non_winner_slot": "R6", "groups": "E/D"},
    # Match 6: W6 vs R5
    6: {"winner_slot": "W6", "non_winner_slot": "R5", "groups": "F/C"},
    # Match 7: W7 vs R8
    7: {"winner_slot": "W7", "non_winner_slot": "R8", "groups": "G/B"},
    # Match 8: W8 vs R7
    8: {"winner_slot": "W8", "non_winner_slot": "R7", "groups": "H/A"},
    
    # Match 9: W9 vs 3rd (from specific groups)
    9: {"winner_slot": "W9", "non_winner_slot": "3RD_1", "groups": "I/K"},
    # Match 10: W10 vs 3rd
    10: {"winner_slot": "W10", "non_winner_slot": "3RD_2", "groups": "J/L"},
    # Match 11: W11 vs 3rd
    11: {"winner_slot": "W11", "non_winner_slot": "3RD_3", "groups": "K/I"},
    # Match 12: W12 vs 3rd
    12: {"winner_slot": "W12", "non_winner_slot": "3RD_4", "groups": "L/J"},
    
    # Match 13: R9 vs 3rd
    13: {"winner_slot": "R9", "non_winner_slot": "3RD_5", "groups": "I/K"},
    # Match 14: R10 vs 3rd
    14: {"winner_slot": "R10", "non_winner_slot": "3RD_6", "groups": "J/L"},
    # Match 15: R11 vs 3rd
    15: {"winner_slot": "R11", "non_winner_slot": "3RD_7", "groups": "K/I"},
    # Match 16: R12 vs 3rd
    16: {"winner_slot": "R12", "non_winner_slot": "3RD_8", "groups": "L/J"},
}

# Reverse mapping: which match slots do teams from each group go to
GROUP_TO_MATCH_SLOTS = {
    "A": [1, 8],
    "B": [2, 7],
    "C": [3, 6],
    "D": [4, 5],
    "E": [5, 4],
    "F": [6, 3],
    "G": [7, 2],
    "H": [8, 1],
    "I": [9, 13],
    "J": [10, 14],
    "K": [11, 15],
    "L": [12, 16],
}


def get_match_info(match_number):
    """
    Get all possible matchups for a given Round of 32 match.
    
    Args:
        match_number: 1-16 (the match slot)
    
    Returns:
        dict with match info and possible team pairings
    """
    if match_number < 1 or match_number > 16:
        return {"error": f"Invalid match number. Must be 1-16."}
    
    bracket = BRACKET_STRUCTURE[match_number]
    qualified = get_qualified_teams()
    
    # Map slot names to actual teams
    slot_to_group = {f"W{i}": chr(64 + i) for i in range(1, 13)}  # W1->A, W2->B, etc
    slot_to_group.update({f"R{i}": chr(64 + i) for i in range(1, 13)})  # R1->A, R2->B, etc
    
    winner_slot = bracket["winner_slot"]
    non_winner_slot = bracket["non_winner_slot"]
    
    # Extract group from slot
    if winner_slot.startswith("W"):
        group_num = int(winner_slot[1:])
        winner_group = chr(64 + group_num)
        team1_group = winner_group
        team1_name = qualified["winners"][group_num - 1]["team"]
    elif winner_slot.startswith("R"):
        group_num = int(winner_slot[1:])
        winner_group = chr(64 + group_num)
        team1_group = winner_group
        team1_name = qualified["runners_up"][group_num - 1]["team"]
    
    # Determine non-winner team
    if non_winner_slot.startswith("R"):
        group_num = int(non_winner_slot[1:])
        non_winner_group = chr(64 + group_num)
        team2_name = qualified["runners_up"][group_num - 1]["team"]
    elif non_winner_slot.startswith("3RD"):
        third_place_rank = int(non_winner_slot.split("_")[1])
        team2_name = qualified["third_place"][third_place_rank - 1]["team"]
        non_winner_group = qualified["third_place"][third_place_rank - 1]["group"]
    
    return {
        "match": match_number,
        "team1": team1_name,
        "team1_group": team1_group,
        "team1_slot": winner_slot,
        "team2": team2_name,
        "team2_group": non_winner_group,
        "team2_slot": non_winner_slot,
        "matchup": f"{team1_name} vs {team2_name}",
        "bracket_info": bracket,
    }


def get_all_r32_matches():
    """Get all 16 Round of 32 matches with confirmed matchups."""
    matches = []
    for match_num in range(1, 17):
        matches.append(get_match_info(match_num))
    return matches
