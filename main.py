"""Main simulation engine interface."""

from group_stage import (
    calculate_standings,
    get_group_winners_and_runners_up,
    get_third_place_teams,
    get_qualified_teams,
)
from bracket_mapper import get_match_info, get_all_r32_matches


def print_group_standings():
    """Print final standings for all groups."""
    print("\n" + "=" * 80)
    print("GROUP STAGE FINAL STANDINGS")
    print("=" * 80)
    
    for group_letter in "ABCDEFGHIJKL":
        standings = calculate_standings(group_letter)
        print(f"\nGroup {group_letter}")
        print("-" * 80)
        print(f"{'Pos':<4} {'Team':<20} {'P':<3} {'W':<2} {'D':<2} {'L':<2} {'GF':<3} {'GA':<3} {'GD':<4} {'Pts':<4}")
        print("-" * 80)
        
        for team in standings:
            print(
                f"{team['position']:<4} {team['team']:<20} {3:<3} "
                f"{team['wins']:<2} {team['draws']:<2} {team['losses']:<2} "
                f"{team['gf']:<3} {team['ga']:<3} {team['gd']:<4} {team['points']:<4}"
            )


def print_qualified_teams():
    """Print all 32 qualified teams."""
    qualified = get_qualified_teams()
    
    print("\n" + "=" * 80)
    print("QUALIFIED TEAMS FOR ROUND OF 32")
    print("=" * 80)
    
    print("\nGROUP WINNERS (1st place)")
    print("-" * 40)
    for i, entry in enumerate(qualified["winners"], 1):
        print(f"{i:2}. Group {entry['group']}: {entry['team']}")
    
    print("\nGROUP RUNNERS-UP (2nd place)")
    print("-" * 40)
    for i, entry in enumerate(qualified["runners_up"], 1):
        print(f"{i:2}. Group {entry['group']}: {entry['team']}")
    
    print("\nBEST 3RD PLACE TEAMS (8 qualified)")
    print("-" * 40)
    for entry in qualified["third_place"]:
        print(
            f"{entry['third_place_rank']}. Group {entry['group']}: {entry['team']} "
            f"({entry['points']} pts, GD {entry['gd']})"
        )


def print_round_of_32_bracket():
    """Print all Round of 32 matches."""
    matches = get_all_r32_matches()
    
    print("\n" + "=" * 80)
    print("ROUND OF 32 BRACKET")
    print("=" * 80)
    
    for i in range(1, 17):
        match = [m for m in matches if m["match"] == i][0]
        print(
            f"\nMatch {i:2}: {match['team1']:<20} ({match['team1_slot']}) "
            f"vs {match['team2']:<20} ({match['team2_slot']})"
        )


def query_match(match_num):
    """Query a specific match."""
    if match_num < 1 or match_num > 16:
        print(f"Error: Match number must be between 1 and 16.")
        return
    
    match = get_match_info(match_num)
    
    print("\n" + "=" * 80)
    print(f"ROUND OF 32 - MATCH {match_num}")
    print("=" * 80)
    print(f"\n{match['team1']} (Group {match['team1_group']}, {match['team1_slot']})")
    print(f"  vs")
    print(f"{match['team2']} (Group {match['team2_group']}, {match['team2_slot']})")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args]")
        print("\nCommands:")
        print("  standings    - Show all group stage standings")
        print("  qualified    - Show all 32 qualified teams")
        print("  bracket      - Show full Round of 32 bracket")
        print("  match <num>  - Show details for a specific match (1-16)")
        print("\nExample: python main.py match 1")
        return
    
    command = sys.argv[1]
    
    if command == "standings":
        print_group_standings()
    elif command == "qualified":
        print_qualified_teams()
    elif command == "bracket":
        print_round_of_32_bracket()
    elif command == "match":
        if len(sys.argv) < 3:
            print("Error: Please specify match number (1-16)")
            return
        try:
            match_num = int(sys.argv[2])
            query_match(match_num)
        except ValueError:
            print("Error: Match number must be an integer")
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
