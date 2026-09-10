import pandas as pd
from matching_player import (result_matched_players,get_understat_club_players,bundesliga_understat,laliga_understat,
                             bundesliga_fotmob,
                             normalize_name,
                             laliga_fotmob
)

players_df=pd.DataFrame(result_matched_players)

players_df["player_key"]=range(1, len(players_df) + 1)

# print(players_df["transfermarkt_club"])
# print(
#     players_df[
#         [
#             "player_key",
#             "player_name",
#             "league",
#             "transfermarkt_club",
#             "understat_id",
#             "fotmob_id"
#         ]
#     ].to_string(index=False)
# )
unmatched_bundesliga = players_df[
    (players_df["league"] == "Bundesliga") &
    (players_df["understat_id"].isna())
]

# print(
#     unmatched_bundesliga[
#         ["player_key", "player_name", "transfermarkt_club"]
#     ].to_string(index=False)
# )

# for _, row in unmatched_bundesliga.iterrows():
#     club = row["transfermarkt_club"]
    
#     print(f"\n{row['player_name']} -> {club}")
    
#     club_players = get_understat_club_players(
#         club,
#         bundesliga_understat
#     )
    
#     print(club_players)

manual_understat_matches = {
    "Maycon Cardozo": "Maycon Douglas Cardozo",
    "Alexander Røssing-Lelesiit": "Alexander Røssing-Lelesiit",
    "Fábio Baldé": "Fabio Baldé",
    "Bazoumana Touré": "Bazoumana Touré",
    "Linus Güther": "Linus Güther",
    "Ismaël Gharbi": "Ismaël Gharbi"
}

understat_name_lookup = {
    player["player_name"]: player
    for player in bundesliga_understat
}

# for tm_name, understat_name in manual_understat_matches.items():
#     player = understat_name_lookup.get(understat_name)

#     print(
#         tm_name,
#         "->",
#         player["player_name"],
#         "| ID:",
#         player["id"]
#     )
    
    
for tm_name, understat_name in manual_understat_matches.items():
    understat = understat_name_lookup.get(understat_name)

    mask = players_df["player_name"] == tm_name

    players_df.loc[mask, "understat_id"] = understat["id"]
    players_df.loc[mask, "understat_name"] = understat["player_name"]
    players_df.loc[mask, "games"] = understat["games"]
    players_df.loc[mask, "minutes"] = understat["time"]
    players_df.loc[mask, "goals"] = understat["goals"]
    players_df.loc[mask, "xG"] = understat["xG"]
    players_df.loc[mask, "assists"] = understat["assists"]
    players_df.loc[mask, "xA"] = understat["xA"]
    players_df.loc[mask, "shots"] = understat["shots"]
    players_df.loc[mask, "key_passes"] = understat["key_passes"]
    players_df.loc[mask, "npxG"] = understat["npxG"]
    
# print(
#     players_df[
#         players_df["player_name"].isin(manual_understat_matches.keys())
#     ][
#         ["player_key", "player_name", "understat_id", "understat_name",
#          "games", "minutes", "goals", "xG"]
#     ].to_string(index=False)
# )

# print("Understat IDs:", players_df["understat_id"].notna().sum())
# print("Understat missing:", players_df["understat_id"].isna().sum())


# print(
#     players_df[
#         players_df["understat_id"].notna()
#     ][
#         ["player_key", "player_name", "understat_id", "understat_name"]
#     ].to_string(index=False)
# )
# print(players_df.shape)

# print(
#     players_df[
#         players_df["player_key"].isin([5, 7, 8, 13, 19, 25])
#     ][
#         [
#             "player_key",
#             "player_name",
#             "transfermarkt_code",
#             "understat_id"
#         ]
#     ].to_string(index=False)
# )

manual_understat_ids = {
    5: "14505",
    7: "13926",
    8: "14036",
    13: "13427",
    19: "14567",
    25: "9766"
}

for player_key, understat_id in manual_understat_ids.items():
    players_df.loc[
        players_df["player_key"] == player_key,
        "understat_id"
    ] = understat_id
    
# print(
#     players_df[
#         players_df["player_key"].isin(manual_understat_ids.keys())
#     ][
#         ["player_key", "player_name", "understat_id"]
#     ].to_string(index=False)
# )


# print("Understat IDs:", players_df["understat_id"].notna().sum())
# print("Understat missing:", players_df["understat_id"].isna().sum())

# print(
#     players_df[
#         players_df["player_key"].isin([5, 7, 8, 13, 19, 25])
#     ][
#         ["player_key", "player_name", "understat_id"]
#     ].to_string(index=False)
# )

# print(
#     players_df[
#         players_df["understat_id"].isna()
#     ][
#         ["player_key", "player_name", "league", "transfermarkt_club"]
#     ].to_string(index=False)
# )

remaining_understat = players_df[
    players_df["understat_id"].isna()
]

for _, row in remaining_understat.iterrows():
    club_players = get_understat_club_players(
        row["transfermarkt_club"],
        bundesliga_understat
    )

    # print(
    #     row["player_name"],
    #     "|",
    #     row["transfermarkt_club"],
    #     "|",
    #     "Understat club players:",
    #     len(club_players)
    # )
    
# for player in bundesliga_understat:
#     if player["team_title"] not in []:
#         print(player["team_title"])

club_name_mapping = {
    "VfB Stuttgart": "VfB Stuttgart",
    "Borussia Dortmund": "Borussia Dortmund",
    "Bayer 04 Leverkusen": "Bayer Leverkusen",
    "RB Leipzig": "RasenBallsport Leipzig",
    "TSG 1899 Hoffenheim": "Hoffenheim",
    "Eintracht Frankfurt": "Eintracht Frankfurt",
    "VfL Wolfsburg": "Wolfsburg",
    "FC Augsburg": "Augsburg",
}

# for tm_club, understat_club in club_name_mapping.items():
#     print(tm_club, "->", understat_club)

for tm_club, understat_club in club_name_mapping.items():
    players = get_understat_club_players(
        understat_club,
        bundesliga_understat
    )

    # print(f"\n{tm_club} -> {understat_club}")
    # print(players)


club_players = get_understat_club_players(
    "VfB Stuttgart",
    bundesliga_understat
)

# print(club_players)

# for player in bundesliga_understat:
#     if player["team_title"] == "VfB Stuttgart":
#         print(
#             player["player_name"],
#             "| ID:", player["id"]
#         )
remaining_bundesliga = players_df[
    (players_df["league"] == "Bundesliga") &
    (players_df["understat_id"].isna())
]

# for _, row in remaining_bundesliga.iterrows():

#     understat_club = club_name_mapping.get(row["transfermarkt_club"])

#     club_players = get_understat_club_players(
#         understat_club,
#         bundesliga_understat
#     )

    # print(
    #     row["player_name"],
    #     "|",
    #     row["transfermarkt_club"],
    #     "| Understat club:",
    #     understat_club,
    #     "| Player found:",
    #     row["player_name"] in club_players
    # )        
    
remaining_laliga = players_df[
    (players_df["league"] == "LaLiga") &
    (players_df["understat_id"].isna())
]

# for _, row in remaining_laliga.iterrows():
#     print(
#         row["player_name"],
#         "|",
#         row["transfermarkt_club"]
#     )    
        
laliga_club_name_mapping = {
    "Athletic Bilbao": "Athletic Club",
    "Celta de Vigo": "Celta Vigo",
    "Real Sociedad": "Real Sociedad",
    "Villarreal CF": "Villarreal",
    "Valencia CF": "Valencia",
    "RCD Espanyol Barcelona": "Espanyol",
    "Deportivo Alavés": "Alaves",
    "CA Osasuna": "Osasuna",
    "Getafe CF": "Getafe",
    "Real Oviedo": "Real Oviedo",
    "Levante UD": "Levante",
}

# for player in laliga_understat:
#     print(player["team_title"])

# for tm_club, understat_club in laliga_club_name_mapping.items():
#     players = get_understat_club_players(
#         understat_club,
#         laliga_understat
#     )

#     print(
#         f"{tm_club} -> {understat_club} | "
#         f"{len(players)} Understat players"
#     )

remaining_laliga = players_df[
    (players_df["league"] == "LaLiga") &
    (players_df["understat_id"].isna())
]

for _, row in remaining_laliga.iterrows():

    understat_club = laliga_club_name_mapping.get(
    row["transfermarkt_club"]
    )

    if understat_club is None:
        # print(
        # row["player_name"],
        # "|",
        # row["transfermarkt_club"],
        # "| No club mapping found"
        # )
        continue

    club_players = get_understat_club_players(
        understat_club,
        laliga_understat
    )

    # print(
    #     row["player_name"],
    #     "|",
    #     row["transfermarkt_club"],
    #     "| Understat club:",
    #     understat_club,
    #     "| Player found:",
    #     row["player_name"] in club_players
    # )
    
laliga_club_name_mapping["Deportivo Alavï¿½s"] = "Alaves"
# print(
#     laliga_club_name_mapping.get("Deportivo Alavï¿½s")
# )


# print(
#     players_df["fotmob_id"].notna().sum(),
#     "of",
#     len(players_df),
#     "players have a FotMob ID"
# )

# print(
#     players_df[
#         players_df["fotmob_id"].isna()
#     ][["player_key", "player_name", "league", "transfermarkt_club"]]
# )

# for player in bundesliga_fotmob:
#     print(
#         player["ParticipantName"],
#         "|",
#         player["TeamName"]
#     )
remaining_fotmob_bundesliga = players_df[
    (players_df["league"] == "Bundesliga") &
    (players_df["fotmob_id"].isna())
]

# for _, row in remaining_fotmob_bundesliga.iterrows():

#     matches = [
#         player
#         for player in bundesliga_fotmob
#         if normalize_name(player["ParticipantName"])
#         == normalize_name(row["player_name"])
#     ]

#     print(
#         row["player_name"],
#         "| Matches:",
#         [m["ParticipantName"] for m in matches]
#     )

# for _, row in remaining_fotmob_bundesliga.iterrows():

#     club_players = [
#         player["ParticipantName"]
#         for player in bundesliga_fotmob
#         if normalize_name(player["TeamName"])
#         == normalize_name(row["transfermarkt_club"])
#     ]

#     print(
#         row["player_name"],
#         "|",
#         row["transfermarkt_club"],
#         "| FotMob club players:",
#         len(club_players)
#     )

fotmob_club_name_mapping = {
    "Bayern Munich": "Bayern München",
    "1.FC Union Berlin": "1. FC Union Berlin",
    "1.FC Heidenheim 1846": "1. FC Heidenheim 1846",
}
# for tm_club, fotmob_club in fotmob_club_name_mapping.items():
#     club_players = [
#         player["ParticipantName"]
#         for player in bundesliga_fotmob
#         if normalize_name(player["TeamName"])
#         == normalize_name(fotmob_club)
#     ]

#     print(
#         tm_club,
#         "->",
#         fotmob_club,
#         "|",
#         len(club_players),
#         "FotMob players"
#     )

id="6e7m0w"
special_bundesliga = players_df[
    players_df["player_key"].isin([4, 5, 19, 23])
]

# for _, row in special_bundesliga.iterrows():

#     fotmob_club = fotmob_club_name_mapping.get(
#         row["transfermarkt_club"]
#     )

#     club_players = [
#         player["ParticipantName"]
#         for player in bundesliga_fotmob
#         if normalize_name(player["TeamName"])
#         == normalize_name(fotmob_club)
#     ]

#     print(
#         "\n",
#         row["player_name"],
#         "| FotMob club:", fotmob_club
#     )
#     print(club_players)
    
    
matched_fotmob = players_df[
    (players_df["league"] == "Bundesliga") &
    (players_df["fotmob_id"].notna())
]

# for _, row in matched_fotmob.iterrows():
#     print(
#         row["player_name"],
#         "|",
#         row["transfermarkt_club"],
#         "|",
#         row["fotmob_name"],
#         "|",
#         row["fotmob_id"]
#     )    


remaining_fotmob_laliga = players_df[
    (players_df["league"] == "LaLiga") &
    (players_df["fotmob_id"].isna())
]

# for _, row in remaining_fotmob_laliga.iterrows():
#     print(row["player_name"], "|", row["transfermarkt_club"])

# for _, row in remaining_fotmob_laliga.iterrows():

#     club_players = [
#         player["ParticipantName"]
#         for player in laliga_fotmob
#         if normalize_name(player["TeamName"])
#         == normalize_name(row["transfermarkt_club"])
#     ]

#     print(
#         row["player_name"],
#         "|",
#         row["transfermarkt_club"],
#         "| FotMob club players:",
#         len(club_players)
#     )

players_to_check = [
    "Hugo ï¿½lvarez",
    "ï¿½ngel Arcos",
    "Wesley",
    "Alex Marchal",
    "Arkaitz Mariezkurrena",
    "Pablo Lï¿½pez",
    "Thiago Fernï¿½ndez"
]

for _, row in remaining_fotmob_laliga.iterrows():

    if row["player_name"] not in players_to_check:
        continue

    club_players = [
        player["ParticipantName"]
        for player in laliga_fotmob
        if normalize_name(player["TeamName"])
        == normalize_name(row["transfermarkt_club"])
    ]

    # print("\n", row["player_name"], "|", row["transfermarkt_club"])
    # print(club_players)

club_players = [
    player["ParticipantName"]
    for player in laliga_fotmob
    if normalize_name(player["TeamName"])
    == normalize_name("Real Sociedad")
]

# print(club_players)

# Show the unique FotMob club names containing Athletic or Girona

# for player in laliga_fotmob:
#     if "athletic" in normalize_name(player["TeamName"]) or \
#        "girona" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])
# for tm_club, fotmob_club in {
#     "Athletic Bilbao": "Athletic Club",
#     "Girona FC": "Girona"
# }.items():

    # club_players = [
    #     player["ParticipantName"]
    #     for player in laliga_fotmob
    #     if normalize_name(player["TeamName"])
    #     == normalize_name(fotmob_club)
    # ]

    # print("\n", tm_club, "->", fotmob_club)
    # print(club_players)

# for player in laliga_fotmob:
#     if "villarreal" in normalize_name(player["TeamName"]):
#         # print(player["TeamName"])
        
# club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Villarreal")
# ]

# # print(club_players)

# for player in laliga_fotmob:
#     if "espanyol" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])


# club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Espanyol")
# ]

# print(club_players)

# for player in laliga_fotmob:
#     if "alaves" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])
        
#         club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Alavés")
# ]

# print(club_players)

# for player in laliga_fotmob:
#     if "osasuna" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])

# club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Osasuna")
# ]

# print(club_players)

for player in laliga_fotmob:
    if (
        normalize_name(player["TeamName"]) == normalize_name("Osasuna")
        and normalize_name(player["ParticipantName"]) == normalize_name("Víctor Muñoz")
    ):
        print()


players_df["fotmob_id"] = players_df["fotmob_id"].astype("Int64").astype("string")

players_df.loc[
    players_df["player_key"] == 46,
    "fotmob_id"
] = "1553105"

# print(
#     players_df.loc[
#         players_df["player_key"] == 46,
#         ["player_name", "fotmob_id"]
#     ]
# )


# for player in laliga_fotmob:
#     if "getafe" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])


# club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Getafe")
# ]

# # print(club_players)

# for player in laliga_fotmob:
#     if (
#         normalize_name(player["TeamName"]) == normalize_name("Getafe")
#         and normalize_name(player["ParticipantName"]) == normalize_name("Adrián Liso")
#     ):
#         print(player["ParticipantName"], "|", player["ParticiantId"])
        
players_df.loc[
    players_df["player_key"] == 47,
    "fotmob_id"
] = "1541825"


# for player in laliga_fotmob:
#     if "levante" in normalize_name(player["TeamName"]):
#         print(player["TeamName"])
    
# club_players = [
#     player["ParticipantName"]
#     for player in laliga_fotmob
#     if normalize_name(player["TeamName"])
#     == normalize_name("Levante")
# ]

# print(club_players)


# print(
#     players_df.groupby("league")["fotmob_id"]
#     .apply(lambda x: x.notna().sum())
# )

# print("\nTotal matched:", players_df["fotmob_id"].notna().sum())
# print("Total unmatched:", players_df["fotmob_id"].isna().sum())


# print(
#     players_df[
#         players_df["fotmob_id"].notna()
#     ][
#         ["player_key", "player_name", "league", "transfermarkt_club", "fotmob_id"]
#     ].to_string(index=False)
# )

players_df = players_df.rename(
    columns={"transfermarket_code": "transfermarkt_code"}
)

# print(players_df.columns.tolist())


import json

# path = "data/raw/fotmob/bundesliga_2025_26/Goals.json"

# with open(path, "r", encoding="utf-8") as file:
#     data = json.load(file)

# print(type(data))
# print(data.keys())

# path = "data/raw/fotmob/bundesliga_2025_26/xG.json"

# with open(path, "r", encoding="utf-8") as file:
#     xg_data = json.load(file)

# print(xg_data["TopLists"][0]["StatList"][0])