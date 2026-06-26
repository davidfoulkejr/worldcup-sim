"""Monte Carlo simulation engine for World Cup 2026 Round-of-32 scenarios."""

from __future__ import annotations

import csv
import json
import math
import random
import re
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from io import StringIO

OPENFOOTBALL_URL = (
    "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
)
ELO_TSV_URL = "https://www.eloratings.net/World.tsv"

# Mapping of openfootball team names to eloratings.net country codes.
TEAM_NAME_TO_ELO_CODE = {
    "Algeria": "DZ",
    "Argentina": "AR",
    "Australia": "AU",
    "Austria": "AT",
    "Belgium": "BE",
    "Bosnia & Herzegovina": "BA",
    "Brazil": "BR",
    "Canada": "CA",
    "Cape Verde": "CV",
    "Colombia": "CO",
    "Croatia": "HR",
    "Curaçao": "CW",
    "Czech Republic": "CZ",
    "DR Congo": "CD",
    "Ecuador": "EC",
    "Egypt": "EG",
    "England": "EN",
    "France": "FR",
    "Germany": "DE",
    "Ghana": "GH",
    "Haiti": "HT",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ivory Coast": "CI",
    "Japan": "JP",
    "Jordan": "JO",
    "Mexico": "MX",
    "Morocco": "MA",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Norway": "NO",
    "Panama": "PA",
    "Paraguay": "PY",
    "Portugal": "PT",
    "Qatar": "QA",
    "Saudi Arabia": "SA",
    "Scotland": "SC",
    "Senegal": "SN",
    "South Africa": "ZA",
    "South Korea": "KR",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Tunisia": "TN",
    "Turkey": "TR",
    "USA": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
}

TEAM_ALIASES = {
    "Cura�ao": "Curaçao",
    "Curacao": "Curaçao",
}

DRAW_SCORES = [((0, 0), 25), ((1, 1), 45), ((2, 2), 25), ((3, 3), 5)]
WIN_SCORES = [
    ((1, 0), 24),
    ((2, 1), 20),
    ((2, 0), 18),
    ((3, 1), 14),
    ((3, 0), 10),
    ((1, 0), 8),
    ((4, 1), 4),
    ((4, 0), 2),
]


def normalize_team_name(team: str) -> str:
    return TEAM_ALIASES.get(team, team)


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def fetch_elo_ratings(url: str) -> dict[str, float]:
    with urllib.request.urlopen(url, timeout=30) as response:
        text = response.read().decode("utf-8")
    reader = csv.reader(StringIO(text), delimiter="\t")
    ratings: dict[str, float] = {}
    for row in reader:
        if len(row) < 4:
            continue
        code = row[2].strip()
        try:
            rating = float(row[3])
        except ValueError:
            continue
        ratings[code] = rating
    return ratings


def weighted_choice(options: list[tuple[tuple[int, int], int]], rng: random.Random) -> tuple[int, int]:
    total = sum(weight for _, weight in options)
    roll = rng.uniform(0, total)
    upto = 0.0
    for value, weight in options:
        upto += weight
        if roll <= upto:
            return value
    return options[-1][0]


def logistic_win_probability(rating_diff: float) -> float:
    return 1.0 / (1.0 + math.pow(10, -rating_diff / 400.0))


def simulate_score(team1_rating: float, team2_rating: float, rng: random.Random) -> tuple[int, int]:
    diff = team1_rating - team2_rating
    draw_prob = max(0.14, min(0.30, 0.27 - abs(diff) / 2200.0))
    team1_win_prob = logistic_win_probability(diff) * (1.0 - draw_prob)
    roll = rng.random()

    if roll < draw_prob:
        return weighted_choice(DRAW_SCORES, rng)

    if roll < draw_prob + team1_win_prob:
        return weighted_choice(WIN_SCORES, rng)

    away_win = weighted_choice(WIN_SCORES, rng)
    return away_win[1], away_win[0]


def make_team_state(team: str) -> dict:
    return {
        "team": team,
        "played": 0,
        "points": 0,
        "gf": 0,
        "ga": 0,
        "gd": 0,
        "h2h": defaultdict(lambda: {"points": 0, "gf": 0, "ga": 0}),
    }


def apply_result(group_state: dict[str, dict], team1: str, team2: str, g1: int, g2: int) -> None:
    t1 = group_state[team1]
    t2 = group_state[team2]

    t1["played"] += 1
    t2["played"] += 1
    t1["gf"] += g1
    t1["ga"] += g2
    t2["gf"] += g2
    t2["ga"] += g1
    t1["gd"] = t1["gf"] - t1["ga"]
    t2["gd"] = t2["gf"] - t2["ga"]

    if g1 > g2:
        t1["points"] += 3
        t1["h2h"][team2]["points"] += 3
    elif g1 < g2:
        t2["points"] += 3
        t2["h2h"][team1]["points"] += 3
    else:
        t1["points"] += 1
        t2["points"] += 1
        t1["h2h"][team2]["points"] += 1
        t2["h2h"][team1]["points"] += 1

    t1["h2h"][team2]["gf"] += g1
    t1["h2h"][team2]["ga"] += g2
    t2["h2h"][team1]["gf"] += g2
    t2["h2h"][team1]["ga"] += g1


def h2h_points(team: dict, tied_teams: list[dict]) -> int:
    tied_names = {t["team"] for t in tied_teams}
    return sum(
        record["points"]
        for opponent, record in team["h2h"].items()
        if opponent in tied_names and opponent != team["team"]
    )


def h2h_goal_difference(team: dict, tied_teams: list[dict]) -> int:
    tied_names = {t["team"] for t in tied_teams}
    return sum(
        record["gf"] - record["ga"]
        for opponent, record in team["h2h"].items()
        if opponent in tied_names and opponent != team["team"]
    )


def h2h_goals_for(team: dict, tied_teams: list[dict]) -> int:
    tied_names = {t["team"] for t in tied_teams}
    return sum(
        record["gf"]
        for opponent, record in team["h2h"].items()
        if opponent in tied_names and opponent != team["team"]
    )


def rank_tied_bucket(bucket: list[dict], criterion_index: int = 0) -> list[dict]:
    # 2026 ordering in-group: points, h2h points, h2h GD, h2h GF, overall GD, overall GF.
    criteria = [
        ("points", True, lambda t, _: t["points"]),
        ("h2h_points", True, h2h_points),
        ("h2h_gd", True, h2h_goal_difference),
        ("h2h_gf", True, h2h_goals_for),
        ("overall_gd", True, lambda t, _: t["gd"]),
        ("overall_gf", True, lambda t, _: t["gf"]),
        ("name", False, lambda t, _: t["team"]),
    ]

    if len(bucket) <= 1 or criterion_index >= len(criteria):
        return sorted(bucket, key=lambda t: t["team"])

    _, descending, value_fn = criteria[criterion_index]
    values: dict[str, float | str] = {team["team"]: value_fn(team, bucket) for team in bucket}
    distinct = sorted(
        {values[team["team"]] for team in bucket},
        reverse=descending,
    )

    ranked: list[dict] = []
    for value in distinct:
        subgroup = [team for team in bucket if values[team["team"]] == value]
        if len(subgroup) == 1:
            ranked.extend(subgroup)
        else:
            ranked.extend(rank_tied_bucket(subgroup, criterion_index + 1))
    return ranked


def rank_group(group_state: dict[str, dict]) -> list[dict]:
    return rank_tied_bucket(list(group_state.values()), criterion_index=0)


def parse_team_slot(slot: str) -> dict[str, object]:
    rank_slot = re.match(r"^([12])([A-L])$", slot)
    if rank_slot:
        return {"kind": "group_rank", "rank": int(rank_slot.group(1)), "group": rank_slot.group(2)}

    third_slot = re.match(r"^3([A-L](?:/[A-L])*)$", slot)
    if third_slot:
        return {"kind": "third_from", "groups": third_slot.group(1).split("/")}

    return {"kind": "team", "team": normalize_team_name(slot)}


def resolve_slot(
    slot: str,
    group_rankings: dict[str, list[dict]],
    third_ranked: list[dict],
    used_third_groups: set[str],
) -> tuple[str, str | None]:
    parsed = parse_team_slot(slot)
    kind = parsed["kind"]

    if kind == "group_rank":
        group = parsed["group"]
        rank = parsed["rank"]
        team_info = group_rankings[group][rank - 1]
        return team_info["team"], group

    if kind == "third_from":
        candidate_groups = set(parsed["groups"])
        for team in third_ranked:
            group = team["group"]
            if group in candidate_groups and group not in used_third_groups:
                used_third_groups.add(group)
                return team["team"], group
        for team in third_ranked:
            if team["group"] in candidate_groups:
                return team["team"], team["group"]
        return "TBD", None

    return parsed["team"], None


def median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def get_team_rating(
    team: str,
    elo_ratings: dict[str, float],
    fallback_rating: float,
    missing_teams: set[str],
) -> float:
    normalized = normalize_team_name(team)
    code = TEAM_NAME_TO_ELO_CODE.get(normalized)
    if code and code in elo_ratings:
        return elo_ratings[code]
    missing_teams.add(normalized)
    return fallback_rating


def deep_copy_group_state(base_state: dict[str, dict[str, dict]]) -> dict[str, dict[str, dict]]:
    copied: dict[str, dict[str, dict]] = {}
    for group, teams in base_state.items():
        copied[group] = {}
        for name, state in teams.items():
            clone = {
                "team": state["team"],
                "played": state["played"],
                "points": state["points"],
                "gf": state["gf"],
                "ga": state["ga"],
                "gd": state["gd"],
                "h2h": defaultdict(lambda: {"points": 0, "gf": 0, "ga": 0}),
            }
            for opponent, record in state["h2h"].items():
                clone["h2h"][opponent] = {
                    "points": record["points"],
                    "gf": record["gf"],
                    "ga": record["ga"],
                }
            copied[group][name] = clone
    return copied


def build_base_state(group_matches: list[dict]) -> tuple[dict[str, dict[str, dict]], list[dict]]:
    groups: dict[str, set[str]] = defaultdict(set)
    for match in group_matches:
        groups[match["group"]].add(match["team1"])
        groups[match["group"]].add(match["team2"])

    state: dict[str, dict[str, dict]] = {}
    for group, teams in groups.items():
        state[group] = {team: make_team_state(team) for team in teams}

    unresolved: list[dict] = []
    for match in group_matches:
        score = match.get("score")
        if score is None:
            unresolved.append(match)
            continue
        apply_result(
            state[match["group"]],
            match["team1"],
            match["team2"],
            score[0],
            score[1],
        )
    return state, unresolved


def extract_matches(raw_matches: list[dict]) -> tuple[list[dict], list[dict]]:
    group_matches: list[dict] = []
    r32_matches: list[dict] = []

    for match in raw_matches:
        if str(match.get("group", "")).startswith("Group "):
            team1 = normalize_team_name(match["team1"])
            team2 = normalize_team_name(match["team2"])
            group = str(match["group"]).split()[-1]
            score = None
            if isinstance(match.get("score"), dict):
                ft = match["score"].get("ft")
                if isinstance(ft, list) and len(ft) == 2:
                    score = (int(ft[0]), int(ft[1]))
            group_matches.append(
                {
                    "group": group,
                    "team1": team1,
                    "team2": team2,
                    "score": score,
                }
            )
        elif match.get("round") == "Round of 32":
            r32_matches.append(
                {
                    "match_num": int(match["num"]),
                    "date": match["date"],
                    "time": match["time"],
                    "ground": match["ground"],
                    "slot1": normalize_team_name(match["team1"]),
                    "slot2": normalize_team_name(match["team2"]),
                }
            )

    r32_matches.sort(key=lambda m: m["match_num"])
    return group_matches, r32_matches


def run_simulation(
    simulations: int = 5000,
    seed: int | None = None,
    fixtures_url: str = OPENFOOTBALL_URL,
    ratings_url: str = ELO_TSV_URL,
) -> dict:
    if simulations <= 0:
        raise ValueError("simulations must be > 0")

    rng = random.Random(seed)
    raw_tournament = fetch_json(fixtures_url)
    elo_ratings = fetch_elo_ratings(ratings_url)
    fallback_rating = median(list(elo_ratings.values()))

    group_matches, r32_matches = extract_matches(raw_tournament["matches"])
    base_state, unresolved_group_matches = build_base_state(group_matches)

    match_aggregates: dict[int, dict[str, Counter]] = {
        m["match_num"]: {
            "team1": Counter(),
            "team2": Counter(),
            "pairings": Counter(),
        }
        for m in r32_matches
    }

    missing_rating_teams: set[str] = set()

    for _ in range(simulations):
        group_state = deep_copy_group_state(base_state)

        for match in unresolved_group_matches:
            team1 = match["team1"]
            team2 = match["team2"]
            rating1 = get_team_rating(team1, elo_ratings, fallback_rating, missing_rating_teams)
            rating2 = get_team_rating(team2, elo_ratings, fallback_rating, missing_rating_teams)
            g1, g2 = simulate_score(rating1, rating2, rng)
            apply_result(group_state[match["group"]], team1, team2, g1, g2)

        group_rankings: dict[str, list[dict]] = {}
        third_pool: list[dict] = []
        for group, teams in group_state.items():
            ranked = rank_group(teams)
            group_rankings[group] = ranked
            third = ranked[2]
            third_pool.append(
                {
                    "team": third["team"],
                    "group": group,
                    "points": third["points"],
                    "gd": third["gd"],
                    "gf": third["gf"],
                }
            )

        third_ranked = sorted(
            third_pool,
            key=lambda t: (-t["points"], -t["gd"], -t["gf"], t["team"]),
        )[:8]

        used_third_groups: set[str] = set()
        for match in r32_matches:
            match_num = match["match_num"]
            team1, _ = resolve_slot(match["slot1"], group_rankings, third_ranked, used_third_groups)
            team2, _ = resolve_slot(match["slot2"], group_rankings, third_ranked, used_third_groups)
            pair_key = f"{team1}|||{team2}"

            agg = match_aggregates[match_num]
            agg["team1"][team1] += 1
            agg["team2"][team2] += 1
            agg["pairings"][pair_key] += 1

    output_matches: list[dict] = []
    for match in r32_matches:
        match_num = match["match_num"]
        agg = match_aggregates[match_num]

        team1_options = [
            {"team": team, "probability": count / simulations}
            for team, count in agg["team1"].most_common()
        ]
        team2_options = [
            {"team": team, "probability": count / simulations}
            for team, count in agg["team2"].most_common()
        ]
        matchup_options = []
        for pair, count in agg["pairings"].most_common():
            team1, team2 = pair.split("|||", 1)
            matchup_options.append(
                {
                    "team1": team1,
                    "team2": team2,
                    "probability": count / simulations,
                }
            )
        most_likely = matchup_options[0] if matchup_options else None

        output_matches.append(
            {
                "match_num": match_num,
                "date": match["date"],
                "time": match["time"],
                "ground": match["ground"],
                "slot1": match["slot1"],
                "slot2": match["slot2"],
                "team1_options": team1_options,
                "team2_options": team2_options,
                "matchup_options": matchup_options,
                "most_likely_matchup": most_likely,
                "confidence": most_likely["probability"] if most_likely else 0.0,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "version": "2.0",
        "simulations": simulations,
        "model": "elo-monte-carlo-v1",
        "fixtures_source": fixtures_url,
        "ratings_source": ratings_url,
        "rating_fallback": fallback_rating,
        "missing_rating_teams": sorted(missing_rating_teams),
        "r32_matches": output_matches,
    }
