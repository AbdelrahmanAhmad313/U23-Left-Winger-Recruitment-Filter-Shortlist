import json
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


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

FOTMOB_BUNDESLIGA_PATH=(
    PROJECT_ROOT    
    / "data"
    / "raw"
    / "fotmob"
    /"bundesliga_2025_26"
    / "Goals.json"
)

FOTMOB_LALIGA_PATH=(
    PROJECT_ROOT    
    / "data"
    / "raw"
    / "fotmob"
    /"laliga_2025_26"
    / "Goals.json"
)

def load_json_lines(path):
    """Load a JSONL file where each line contains one JSON object."""
    with open(path, "r", encoding="cp1252") as file:
        return [json.loads(line) for line in file]


def load_understat(path):
    """Load an Understat JSON array."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_fotmob(path):
    """Load an Fotmob JSON array."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    players = []

    for top_list in data["TopLists"]:
        players.extend(top_list["StatList"])

    return players

bundesliga_tm = load_json_lines(TRANSFERMARKT_BUNDESLIGA_PATH)
laliga_tm = load_json_lines(TRANSFERMARKT_LALIGA_PATH)

bundesliga_understat = load_understat(UNDERSTAT_BUNDESLIGA_PATH)
laliga_understat = load_understat(UNDERSTAT_LALIGA_PATH)

bundesliga_fotmob=load_fotmob(FOTMOB_BUNDESLIGA_PATH)
laliga_fotmob=load_fotmob(FOTMOB_LALIGA_PATH)

# print("Transfermarkt Bundesliga:", len(bundesliga_tm))
# print("Transfermarkt LaLiga:", len(laliga_tm))
# print("Understat Bundesliga:", len(bundesliga_understat))
# print("Understat LaLiga:", len(laliga_understat))
# print("Fotmob Bundesliga:", len(bundesliga_fotmob))
# print("Fotmob LaLiga:", len(laliga_fotmob))

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
    
for player in bundesliga_fotmob:
    player["normalized_name"] = normalize_name(
        player["ParticipantName"]
    )
        
for player in laliga_fotmob:
    player["normalized_name"] = normalize_name(
        player["ParticipantName"]
    )    
    
understat_bundesliga_lookup = {
    player["normalized_name"]: player
    for player in bundesliga_understat
}

understat_laliga_lookup = {
    player["normalized_name"]: player
    for player in laliga_understat
}

transfermarkt_bundesliga_lookup = {
    player["normalized_name"]: player
    for player in bundesliga_tm
}

transfermarkt_laliga_lookup = {
    player["normalized_name"]: player
    for player in laliga_tm
}
fotmob_bundesliga_lookup = {
    player["normalized_name"]: player
    for player in bundesliga_fotmob
}

fotmob_laliga_lookup = {
    player["normalized_name"]: player
    for player in laliga_fotmob
}


for player in bundesliga_tm:
    player["understat_match"] = understat_bundesliga_lookup.get(
        player["normalized_name"]
    )

for player in laliga_tm:
    player["understat_match"] = understat_laliga_lookup.get(
        player["normalized_name"]
    )

for player in bundesliga_fotmob:
    player["transfermarkt_match"] = transfermarkt_bundesliga_lookup.get(
        player["normalized_name"]
    )
    
for player in laliga_fotmob:
    player["transfermarkt_match"] = transfermarkt_laliga_lookup.get(
        player["normalized_name"]
    )
    
for player in bundesliga_tm:
    player["fotmob_match"] = fotmob_bundesliga_lookup.get(
        player["normalized_name"]
    )

for player in laliga_tm:
    player["fotmob_match"] = fotmob_laliga_lookup.get(
        player["normalized_name"]
    )

# print(
#     "Bundesliga matched (understat - transfermarkt):",
#     sum(player["understat_match"] is not None for player in bundesliga_tm)
# )

# print(
#     "LaLiga matched (understat - transfermarkt):",
#     sum(player["understat_match"] is not None for player in laliga_tm)
# )

# print(
#     "Bundesliga matched (transfermarkt - Fotmob):",
#     sum(player["transfermarkt_match"] is not None for player in bundesliga_fotmob)
# )

# print(
#     "LaLiga matched (transfermarkt - Fotmob):",
#     sum(player["transfermarkt_match"] is not None for player in laliga_fotmob)
# )

# print("\n--- Unmatched Bundesliga ---")

# print("\n--(understat - transfermarkt)--")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         print(
#             player["name"],
#             player["last_name"],
#             "|",
#             player["normalized_name"]
#         )

# print("\n--(Fotmob - transfermarkt)--")

# for player in bundesliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         print(
#             player["ParticipantName"],
#             "|",
#             player["normalized_name"]
#         )
        
# print("\n--- Unmatched LaLiga ---")

# print("\n--(understat - transfermarkt)--")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         print(
#             player["name"],
#             player["last_name"],
#             "|",
#             player["normalized_name"]
#         )
        
# print("\n--(Fotmob - transfermarkt)--")

# for player in laliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         print(
#             player["ParticipantName"],
#             "|",
#             player["normalized_name"]
#         ) 
        
        
def find_partial_matches(player_name, understat_players):
    normalized = normalize_name(player_name)

    matches = []

    for player in understat_players:
        understat_name = normalize_name(player["player_name"])

        if normalized in understat_name or understat_name in normalized:
            matches.append(player["player_name"])

    return matches

def find_partial_matches_tm(player_name, tm_players):
    normalized = normalize_name(player_name)

    matches = []
    
    for player in tm_players:
        name=f"{player['name']} {player['last_name']}"
        understat_name = normalize_name(name)

        if normalized in understat_name or understat_name in normalized:
            matches.append(name)

    return matches

# print("\n--- Possible Bundesliga matches ---")

# print("\n--(understat - transfermarkt)--")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         name = f'{player["name"]} {player["last_name"]}'
#         matches = find_partial_matches(name, bundesliga_understat)

#         print(name, "->", matches)
        
# print("\n--(Fotmob - transfermarkt)--")

# for player in bundesliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         # name = f'{player["name"]} {player["last_name"]}'
#         matches = find_partial_matches_tm(player["ParticipantName"], bundesliga_tm)

#         print(player["ParticipantName"], "->", matches)

# print("\n--- Possible LaLiga matches ---")

# print("\n--(understat - transfermarkt)--")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         name = f'{player["name"]} {player["last_name"]}'
#         matches = find_partial_matches(name, laliga_understat)

#         print(name, "->", matches)
        
# print("\n--(Fotmob - transfermarkt)--")
        
# for player in laliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         name = player["ParticipantName"]
#         matches = find_partial_matches_tm(name, laliga_tm)

#         print(name, "->", matches)
        
# print("\n--- Unmatched Bundesliga with clubs ---")

# print("\n--(understat - transfermarkt)--")

# for player in bundesliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         name = f'{player["name"]} {player["last_name"]}'
#         print(name, "->", club)

# print("\n--(Fotmob - transfermarkt)--")

# for player in bundesliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         club = player["TeamName"]
#         name = player["ParticipantName"]
#         print(name, "->", club)

# print("\n--- Unmatched LaLiga with clubs ---")

# print("\n--(understat - transfermarkt)--")

# for player in laliga_tm:
#     if player["understat_match"] is None:
#         club = player["parent"]["name"]
#         name = f'{player["name"]} {player["last_name"]}'
#         print(name, "->", club)
        
# print("\n--(Fotmob - transfermarkt)--")

# for player in laliga_fotmob:
#     if player["transfermarkt_match"] is None:
#         club = player["TeamName"]
#         name = player["ParticipantName"]
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

        # print(f"\n{player['name']} {player['last_name']} -> {club}")
        # print("Understat players:", understat_players)
        
        
matched_players = []

for player in bundesliga_tm:
    understat = player.get("understat_match")
    fotmob = player.get("fotmob_match")

    matched_players.append({
        "player_name": f'{player["name"]} {player["last_name"]}',
        "league": "Bundesliga",
        "transfermarkt_club": player["parent"]["name"],
        "transfermarkt_code":player["code"],
        
        "games": understat["games"] if understat is not None else None,
        "minutes": understat["time"] if understat is not None else None,
        "goals": understat["goals"] if understat is not None else None,
        "xG": understat["xG"] if understat is not None else None,
        "assists": understat["assists"] if understat is not None else None,
        "xA": understat["xA"] if understat is not None else None,
        "shots": understat["shots"] if understat is not None else None,
        "key_passes": understat["key_passes"] if understat is not None else None,
        "npxG": understat["npxG"] if understat is not None else None,
        
                "fotmob_name": (
                    fotmob["ParticipantName"]
                    if fotmob is not None
                    else None
                ),
        
                "understat_name": (
                    understat["player_name"]
                    if understat is not None
                    else None
                ),
                
                "understat_team": (
                    understat["team_title"]
                    if understat is not None
                    else None
                ),
                "fotmob_id":(
                                    fotmob["ParticiantId"]
                                    if fotmob is not None
                                    else None
                                ),
                "understat_id":(
                    understat["id"]
                    if understat is not None
                    else None
                ),
        
    })

for player in laliga_tm:
    understat = player.get("understat_match")
    fotmob = player.get("fotmob_match")

    matched_players.append({
        "player_name": f'{player["name"]} {player["last_name"]}',
        "league": "LaLiga",
        "transfermarkt_club": player["parent"]["name"],
        "games": understat["games"] if understat is not None else None,
        "minutes": understat["time"] if understat is not None else None,
        "goals": understat["goals"] if understat is not None else None,
        "xG": understat["xG"] if understat is not None else None,
        "assists": understat["assists"] if understat is not None else None,
        "xA": understat["xA"] if understat is not None else None,
        "shots": understat["shots"] if understat is not None else None,
        "key_passes": understat["key_passes"] if understat is not None else None,
        "npxG": understat["npxG"] if understat is not None else None,
        
                "fotmob_name": (
                    fotmob["ParticipantName"]
                    if fotmob is not None
                    else None
                ),
        
                "understat_name": (
                    understat["player_name"]
                    if understat is not None
                    else None
                ),
                
                "understat_team": (
                    understat["team_title"]
                    if understat is not None
                    else None
                ),
                "fotmob_id":(
                                    fotmob["ParticiantId"]
                                    if fotmob is not None
                                    else None
                                ),
                "understat_id":(
                    understat["id"]
                    if understat is not None
                    else None
                ),
    })
        

result_matched_players= matched_players       

# print("Total matched players:", len(matched_players))
# print(matched_players[:3])

