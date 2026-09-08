import json
import unicodedata
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data paths
TRANSFERMARKT_BUNDESLIGA_PATH = (
    PROJECT_ROOT
    /"data"
    /"raw"
    / "transfermarkt-scraper"
    / "bundesliga_u23_left_wingers_2025_26.json"
)

TRANSFERMARKT_LALIGA_PATH = (
    PROJECT_ROOT
    /"data"
    /"raw"
    / "transfermarkt-scraper"
    / "laliga_u23_left_wingers_2025_26.json"
)

UNDERSTAT_BUNDESLIGA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "understat"
    / "bundesliga_2025_26.json"
)

UNDERSTAT_LALIGA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "understat"
    / "la_liga_2025_26.json"
)


def load_json_lines(path):
    """Load a JSONL file where each line contains one JSON object."""
    with open(path, "r", encoding="cp1252") as file:
        return [json.loads(line) for line in file]


def load_understat(path):
    """Load an Understat JSON array."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


bundesliga_tm = load_json_lines(TRANSFERMARKT_BUNDESLIGA_PATH)
laliga_tm = load_json_lines(TRANSFERMARKT_LALIGA_PATH)

bundesliga_understat = load_understat(UNDERSTAT_BUNDESLIGA_PATH)
laliga_understat = load_understat(UNDERSTAT_LALIGA_PATH)


print("Transfermarkt Bundesliga:", len(bundesliga_tm))
print("Transfermarkt LaLiga:", len(laliga_tm))
print("Understat Bundesliga:", len(bundesliga_understat))
print("Understat LaLiga:", len(laliga_understat))

def normalize_name(name):
    """Normalize a player name for comparison."""
    name = name.strip().lower()

    # Remove accents/diacritics
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        char for char in name
        if not unicodedata.combining(char)
    )

    # Standardize separators
    name = name.replace("-", " ")

    # Remove extra whitespace
    name = " ".join(name.split())

    return name

for player in bundesliga_tm:
    player["normalized_name"] = normalize_name(
        f'{player["name"]} {player["last_name"]}'
    )

for player in laliga_tm:
    player["normalized_name"] = normalize_name(
        f'{player["name"]} {player["last_name"]}'
    )

for player in bundesliga_understat:
    player["normalized_name"] = normalize_name(
        player["player_name"]
    )

for player in laliga_understat:
    player["normalized_name"] = normalize_name(
        player["player_name"]
    )
    
    understat_bundesliga_lookup = {
    player["normalized_name"]: player
    for player in bundesliga_understat
}

understat_laliga_lookup = {
    player["normalized_name"]: player
    for player in laliga_understat
}

for player in bundesliga_tm:
    player["understat_match"] = understat_bundesliga_lookup.get(
        player["normalized_name"]
    )

for player in laliga_tm:
    player["understat_match"] = understat_laliga_lookup.get(
        player["normalized_name"]
    )
    

print(
    "Bundesliga matched:",
    sum(player["understat_match"] is not None for player in bundesliga_tm)
)

print(
    "LaLiga matched:",
    sum(player["understat_match"] is not None for player in laliga_tm)
)

print("\n--- Unmatched Bundesliga ---")

for player in bundesliga_tm:
    if player["understat_match"] is None:
        print(
            player["name"],
            player["last_name"],
            "|",
            player["normalized_name"]
        )


print("\n--- Unmatched LaLiga ---")

for player in laliga_tm:
    if player["understat_match"] is None:
        print(
            player["name"],
            player["last_name"],
            "|",
            player["normalized_name"]
        )
        
        
def find_partial_matches(player_name, understat_players):
    normalized = normalize_name(player_name)

    matches = []

    for player in understat_players:
        understat_name = normalize_name(player["player_name"])

        if normalized in understat_name or understat_name in normalized:
            matches.append(player["player_name"])

    return matches


# print("\n--- Possible Bundesliga matches ---")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         name = f'{player["name"]} {player["last_name"]}'
#         matches = find_partial_matches(name, bundesliga_understat)

#         print(name, "->", matches)


# print("\n--- Possible LaLiga matches ---")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         name = f'{player["name"]} {player["last_name"]}'
#         matches = find_partial_matches(name, laliga_understat)

#         print(name, "->", matches)
        
        
# print("\n--- Unmatched Bundesliga with clubs ---")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         name = f'{player["name"]} {player["last_name"]}'
#         print(name, "->", club)


# print("\n--- Unmatched LaLiga with clubs ---")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         name = f'{player["name"]} {player["last_name"]}'
#         print(name, "->", club)
        
        
def get_understat_club_players(club_name, understat_players):
    return [
        player["player_name"]
        for player in understat_players
        if player["team_title"].lower() in club_name.lower()
        or club_name.lower() in player["team_title"].lower()
    ]
    
# print("\n--- Bundesliga club coverage ---")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         understat_players = get_understat_club_players(
#             club,
#             bundesliga_understat
#         )

#         print(f"\n{player['name']} {player['last_name']} -> {club}")
#         print("Understat players:", understat_players)


# print("\n--- LaLiga club coverage ---")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         understat_players = get_understat_club_players(
#             club,
#             laliga_understat
#         )

#         print(f"\n{player['name']} {player['last_name']} -> {club}")
#         print("Understat players:", understat_players)
        
        
matched_players = []

for player in bundesliga_tm:
    if player["understat_match"] is not None:
        understat = player["understat_match"]

        matched_players.append({
            "player_name": f'{player["name"]} {player["last_name"]}',
            "league": "Bundesliga",
            "transfermarkt_club": player["parent"]["name"],
            "understat_name": understat["player_name"],
            "understat_team": understat["team_title"],
            "games": understat["games"],
            "minutes": understat["time"],
            "goals": understat["goals"],
            "xG": understat["xG"],
            "assists": understat["assists"],
            "xA": understat["xA"],
            "shots": understat["shots"],
            "key_passes": understat["key_passes"],
            "npxG": understat["npxG"]
        })

for player in laliga_tm:
    if player["understat_match"] is not None:
        understat = player["understat_match"]

        matched_players.append({
            "player_name": f'{player["name"]} {player["last_name"]}',
            "league": "LaLiga",
            "transfermarkt_club": player["parent"]["name"],
            "understat_name": understat["player_name"],
            "understat_team": understat["team_title"],
            "games": understat["games"],
            "minutes": understat["time"],
            "goals": understat["goals"],
            "xG": understat["xG"],
            "assists": understat["assists"],
            "xA": understat["xA"],
            "shots": understat["shots"],
            "key_passes": understat["key_passes"],
            "npxG": understat["npxG"]
        })
        

result_matched_players= matched_players       

print("Total matched players:", len(matched_players))
print(matched_players[:3])

