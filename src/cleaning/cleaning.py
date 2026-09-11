import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from understanding.understanding import all_candidates_fotmob
from matching.matching_player import PROJECT_ROOT,TRANSFERMARKT_BUNDESLIGA_PATH,TRANSFERMARKT_LALIGA_PATH,laliga_understat,bundesliga_understat

# print("Searching for Transfermarkt JSON files...")

# for file in Path(PROJECT_ROOT).rglob("*.json"):
#     if "transfermarkt" in str(file).lower():
#         print(file)


all_candidates_fotmob = all_candidates_fotmob.rename(
    columns={
        "games": "understat_games",
        "minutes_x": "understat_minutes",
        "goals_x": "understat_goals",
        "xG_x": "understat_xG",
        "assists_x": "understat_assists",
        "xA_x": "understat_xA",
        "shots": "understat_shots",
        "key_passes": "understat_key_passes",
        "npxG": "understat_npxG",

        "goals_y": "fotmob_goals",
        "assists_y": "fotmob_assists",
        "xG_y": "fotmob_xG",
        "xA_y": "fotmob_xA",
        "minutes_y": "fotmob_minutes",
    }
)

# print(all_candidates_fotmob.columns.tolist())

understat_numeric_columns = [
    "understat_games",
    "understat_minutes",
    "understat_goals",
    "understat_xG",
    "understat_assists",
    "understat_xA",
    "understat_shots",
    "understat_key_passes",
    "understat_npxG"
]

all_candidates_fotmob[understat_numeric_columns] = (
    all_candidates_fotmob[understat_numeric_columns]
    .apply(pd.to_numeric, errors="coerce")
)

# print(all_candidates_fotmob[understat_numeric_columns].dtypes)

# print(all_candidates_fotmob[understat_numeric_columns].isna().sum())

# print(
#     all_candidates_fotmob[
#         ["player_name", "understat_name", "fotmob_name"]
#     ].to_string(index=False)
# )

with open(TRANSFERMARKT_BUNDESLIGA_PATH, "rb") as file:
    raw_data = file.read()

# print("Contains UTF-8 Rø sequence:", b"R\xc3\xb8" in raw_data)
# print("Contains replacement character:", b"\xef\xbf\xbd" in raw_data)
# print("Contains literal ï¿½:", "ï¿½".encode("utf-8") in raw_data)

with open(
    TRANSFERMARKT_LALIGA_PATH,
    "rb"
) as file:
    raw_data_laliga = file.read()

# print("Contains UTF-8 Rø sequence:", b"R\xc3\xb8" in raw_data)
# print("Contains replacement character:", b"\xef\xbf\xbd" in raw_data)
# print("Contains literal ï¿½:", "ï¿½".encode("utf-8") in raw_data)

# print(
#     all_candidates_fotmob[
#         all_candidates_fotmob["player_name"].str.contains("�", na=False)
#     ][["player_name", "understat_name", "fotmob_name"]]
# )

# print(
#     "Corrupted player names:",
#     all_candidates_fotmob["player_name"].str.contains("�", na=False).sum()
# )

# print(
#     all_candidates_fotmob[
#         ["player_name", "understat_name", "fotmob_name"]
#     ].to_string(index=False)
# )

corrupted_names = all_candidates_fotmob[
    all_candidates_fotmob["player_name"].str.contains("�", na=False)
][
    [
        "player_key",
        "player_name",
        "league",
        "transfermarkt_club",
        "transfermarkt_code"
    ]
]

# print(corrupted_names.to_string(index=False))


# print(
#     corrupted_names[
#         ["player_name", "transfermarkt_code"]
#     ].to_string(index=False)
# )

name_corrections = {
    "Alexander R�ssing-Lelesiit": "Alexander Røssing-Lelesiit",
    "F�bio Bald�": "Fábio Baldé",
    "Bazoumana Tour�": "Bazoumana Touré",
    "Jean-Matt�o Bahoya": "Jean-Mattéo Bahoya",
    "Linus G�ther": "Linus Güther",
    "Isma�l Gharbi": "Ismaël Gharbi",
    "Hugo �lvarez": "Hugo Álvarez",
    "�ngel Arcos": "Ángel Arcos",
    "Joselillo Gait�n": "Joselillo Gaitán",
    "Pablo L�pez": "Pablo López",
    "Izei Hern�ndez": "Izei Hernández",
    "V�ctor Mu�oz": "Víctor Muñoz",
    "Adri�n Liso": "Adrián Liso",
    "Thiago Fern�ndez": "Thiago Fernández",
    "Paco Cort�s": "Paco Cortés"
}

all_candidates_fotmob["player_name"] = (
    all_candidates_fotmob["player_name"].replace(name_corrections)
)

corrupted_names = all_candidates_fotmob[
    all_candidates_fotmob["player_name"].str.contains("�", na=False)
][
    ["player_name", "transfermarkt_code"]
]

# print(corrupted_names)

# print(f"Corrupted names remaining: {len(corrupted_names)}")


duplicate_players = all_candidates_fotmob[
    all_candidates_fotmob.duplicated(
        subset=["league", "player_name"],
        keep=False
    )
].sort_values(["league", "player_name"])

# print(duplicate_players[
#     ["league", "player_name", "transfermarkt_code"]
# ])

# print(
#     f"Duplicate player records: {len(duplicate_players)}"
# )

both_sources = all_candidates_fotmob[
    all_candidates_fotmob["data_group"] == "Both"
].copy()

# print(
#     both_sources[
#         [
#             "player_name",
#             "understat_name",
#             "fotmob_name",
#             "transfermarkt_club",
#             "understat_team",
#             "fotmob_id",
#             "understat_id"
#         ]
#     ].to_string(index=False)
# )

club_encoding_check = all_candidates_fotmob[
    all_candidates_fotmob["transfermarkt_club"].str.contains("�", na=False)
][
    ["player_name", "transfermarkt_club", "understat_team"]
]

# print(club_encoding_check.to_string(index=False))
# print(f"\nCorrupted Transfermarkt club names: {len(club_encoding_check)}")

club_corrections = {
    "1.FC K�ln": "1.FC Köln",
    "Borussia M�nchengladbach": "Borussia Mönchengladbach",
    "Deportivo Alav�s": "Deportivo Alavés"
}

all_candidates_fotmob["transfermarkt_club"] = (
    all_candidates_fotmob["transfermarkt_club"].replace(club_corrections)
)

corrupted_clubs = all_candidates_fotmob[
    all_candidates_fotmob["transfermarkt_club"].str.contains("�", na=False)
][
    ["player_name", "transfermarkt_club"]
]

# print(corrupted_clubs)
# print(f"\nCorrupted club names remaining: {len(corrupted_clubs)}")

izei_check = all_candidates_fotmob[
    all_candidates_fotmob["player_name"] == "Izei Hernández"
][
    [
        "player_name",
        "league",
        "transfermarkt_club",
        "understat_name",
        "understat_team",
        "understat_id",
        "fotmob_name",
        "fotmob_id",
        "data_group"
    ]
]

# print(izei_check.to_string(index=False))

laliga_understat_df = pd.DataFrame(laliga_understat)

# print(
#     laliga_understat_df[
#         laliga_understat_df["player_name"].str.contains(
#             "Izei|Hern", case=False, na=False
#         )
#     ].to_string(index=False)
# )
