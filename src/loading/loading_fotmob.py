import json
import pandas as pd
from functools import reduce
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from matching.matching_table import players_df

def load_fotmob_metric(path, metric_name):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    players = []

    for top_list in data["TopLists"]:
        players.extend(top_list["StatList"])

    df = pd.DataFrame(players)

    df = df[
        ["ParticiantId", "ParticipantName", "TeamName", "StatValue"]
    ].rename(
        columns={
            "ParticiantId": "participant_id",
            "StatValue": metric_name
        }
    )

    return df

fotmob_json_metrics = {
    "Goals.json": "goals",
    "Assists.json": "assists",
    "Goals and Assists.json": "goals_and_assists",
    "FotMob rating.json": "fotmob_rating",
    "Minutes played.json": "minutes",
    "Goals per 90.json": "goals_per_90",
    "xG.json": "xG",
    "xG per 90.json": "xG_per_90",
    "xGOT.json": "xGOT",
    "Shots on target per 90 .json": "shots_on_target_per_90",
    "Shots per 90.json": "shots_per_90",
    "Accurate passes per 90 .json": "accurate_passes_per_90",
    "Big chances created.json": "big_chances_created",
    "Chances created.json": "chances_created",
    "Accurate long balls per 90 .json": "accurate_long_balls_per_90",
    "xA.json": "xA",
    "xA per 90.json": "xA_per_90",
    "xG and xA per 90.json": "xG_and_xA_per_90",
    "Successful dribbles per 90.json": "successful_dribbles_per_90",
    "Big chances missed .json": "big_chances_missed",
    "Defensive actions per 90.json": "defensive_actions_per_90",
    "Recoveries per 90.json": "recoveries_per_90",
    "Possession won final 3rd per 90.json": "possession_won_final_3rd_per_90"
}


bundesliga_fotmob_dfs = []

for filename, metric_name in fotmob_json_metrics.items():
    path = f"data/raw/fotmob/bundesliga_2025_26/{filename}"

    df = load_fotmob_metric(path, metric_name)

    # Keep only the ID and the metric we are adding
    df = df[["participant_id", metric_name]]

    bundesliga_fotmob_dfs.append(df)

# print(len(bundesliga_fotmob_dfs))

bundesliga_fotmob = reduce(
    lambda left, right: left.merge(
        right,
        on="participant_id",
        how="outer"
    ),
    bundesliga_fotmob_dfs
)

# print(bundesliga_fotmob.shape)
# print(bundesliga_fotmob.columns.tolist())
# print(bundesliga_fotmob["participant_id"].nunique())

# for filename, metric_name in fotmob_json_metrics.items():
#     path = f"data/raw/fotmob/bundesliga_2025_26/{filename}"

#     df = load_fotmob_metric(path, metric_name)

#     duplicates = df["participant_id"].duplicated().sum()

#     print(filename, "→ duplicates:", duplicates)


bundesliga_candidates = players_df[
    players_df["league"] == "Bundesliga"
].copy()

bundesliga_candidates["fotmob_id"] = (
    bundesliga_candidates["fotmob_id"]
    .astype("string")
)

bundesliga_fotmob["participant_id"] = (
    bundesliga_fotmob["participant_id"]
    .astype("string")
)

bundesliga_candidates_fotmob = bundesliga_candidates.merge(
    bundesliga_fotmob,
    left_on="fotmob_id",
    right_on="participant_id",
    how="left"
)


laliga_fotmob_dfs = []

for filename, metric_name in fotmob_json_metrics.items():
    path = f"data/raw/fotmob/laliga_2025_26/{filename}"

    df = load_fotmob_metric(path, metric_name)

    df = df[["participant_id", metric_name]]

    laliga_fotmob_dfs.append(df)


laliga_fotmob = reduce(
    lambda left, right: left.merge(
        right,
        on="participant_id",
        how="outer"
    ),
    laliga_fotmob_dfs
)

laliga_candidates = players_df[
    players_df["league"] == "LaLiga"
].copy()

laliga_candidates["fotmob_id"] = (
    laliga_candidates["fotmob_id"]
    .astype("string")
)

laliga_fotmob["participant_id"] = (
    laliga_fotmob["participant_id"]
    .astype("string")
)

laliga_candidates_fotmob = laliga_candidates.merge(
    laliga_fotmob,
    left_on="fotmob_id",
    right_on="participant_id",
    how="left"
)

all_candidates_fotmob = pd.concat(
    [
        bundesliga_candidates_fotmob,
        laliga_candidates_fotmob
    ],
    ignore_index=True
)

all_candidates_fotmob["data_group"] = "Neither"

all_candidates_fotmob.loc[
    all_candidates_fotmob["understat_id"].notna()
    & all_candidates_fotmob["fotmob_id"].notna(),
    "data_group"
] = "Both"

all_candidates_fotmob.loc[
    all_candidates_fotmob["understat_id"].notna()
    & all_candidates_fotmob["fotmob_id"].isna(),
    "data_group"
] = "Understat only"

all_candidates_fotmob.loc[
    all_candidates_fotmob["understat_id"].isna()
    & all_candidates_fotmob["fotmob_id"].notna(),
    "data_group"
] = "FotMob only"
neither_players = all_candidates_fotmob[
    all_candidates_fotmob["data_group"] == "Neither"
][
    ["player_key", "player_name", "league", "transfermarkt_club"]
]

all_candidates_fotmob["data_status"] = "Insufficient performance data"

all_candidates_fotmob.loc[
    all_candidates_fotmob["data_group"] != "Neither",
    "data_status"
] = "Performance data available"

# print(all_candidates_fotmob["data_status"].value_counts())
