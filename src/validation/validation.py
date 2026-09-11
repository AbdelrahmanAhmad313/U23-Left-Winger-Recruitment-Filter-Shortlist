import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from cleaning.cleaning import all_candidates_fotmob


understat_value_columns = [
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

fotmob_numeric_columns = [
    "fotmob_goals",
    "fotmob_assists",
    "goals_and_assists",
    "fotmob_rating",
    "fotmob_minutes",
    "goals_per_90",
    "fotmob_xG",
    "xG_per_90",
    "xGOT",
    "shots_on_target_per_90",
    "shots_per_90",
    "accurate_passes_per_90",
    "big_chances_created",
    "chances_created",
    "accurate_long_balls_per_90",
    "fotmob_xA",
    "xA_per_90",
    "xG_and_xA_per_90",
    "successful_dribbles_per_90",
    "big_chances_missed",
    "defensive_actions_per_90",
    "recoveries_per_90",
    "possession_won_final_3rd_per_90"
]

# print(
#     all_candidates_fotmob[fotmob_numeric_columns].dtypes
# )

for column in understat_value_columns:
    invalid = all_candidates_fotmob[
        all_candidates_fotmob[column].notna()
        & (all_candidates_fotmob[column] < 0)
    ]

    # print(f"{column}: {len(invalid)} negative values")
    
    invalid_goals_shots = all_candidates_fotmob[
    all_candidates_fotmob["understat_goals"].notna()
    & all_candidates_fotmob["understat_shots"].notna()
    & (
        all_candidates_fotmob["understat_goals"]
        > all_candidates_fotmob["understat_shots"]
    )
]

# print(
#     invalid_goals_shots[
#         [
#             "player_name",
#             "understat_goals",
#             "understat_shots"
#         ]
#     ].to_string(index=False)
# )

# print(f"\nGoals > shots violations: {len(invalid_goals_shots)}")

invalid_goals_no_shots = all_candidates_fotmob[
    all_candidates_fotmob["understat_goals"].notna()
    & all_candidates_fotmob["understat_shots"].notna()
    & (all_candidates_fotmob["understat_goals"] > 0)
    & (all_candidates_fotmob["understat_shots"] == 0)
]

# print(
#     invalid_goals_no_shots[
#         [
#             "player_name",
#             "understat_goals",
#             "understat_shots"
#         ]
#     ].to_string(index=False)
# )

# print(
#     f"\nGoals > 0 with zero shots: {len(invalid_goals_no_shots)}"
# )

invalid_xg_no_shots = all_candidates_fotmob[
    all_candidates_fotmob["understat_xG"].notna()
    & all_candidates_fotmob["understat_shots"].notna()
    & (all_candidates_fotmob["understat_xG"] > 0)
    & (all_candidates_fotmob["understat_shots"] == 0)
]

# print(
#     invalid_xg_no_shots[
#         [
#             "player_name",
#             "understat_xG",
#             "understat_shots"
#         ]
#     ].to_string(index=False)
# )

# print(
#     f"\nPositive xG with zero shots: {len(invalid_xg_no_shots)}"
# )

invalid_npxg_xg = all_candidates_fotmob[
    all_candidates_fotmob["understat_npxG"].notna()
    & all_candidates_fotmob["understat_xG"].notna()
    & (
        all_candidates_fotmob["understat_npxG"]
        > all_candidates_fotmob["understat_xG"]
    )
]

# print(
#     invalid_npxg_xg[
#         [
#             "player_name",
#             "understat_xG",
#             "understat_npxG"
#         ]
#     ].to_string(index=False)
# )

# print(
#     f"\nnpxG > xG violations: {len(invalid_npxg_xg)}"
# )

performance_columns = [
    "understat_goals",
    "understat_xG",
    "understat_assists",
    "understat_xA",
    "understat_shots",
    "understat_key_passes"
]

invalid_zero_minutes = all_candidates_fotmob[
    all_candidates_fotmob["understat_minutes"].notna()
    & (all_candidates_fotmob["understat_minutes"] == 0)
    & (
        all_candidates_fotmob[performance_columns]
        .fillna(0)
        .sum(axis=1) > 0
    )
]

# print(
#     invalid_zero_minutes[
#         ["player_name", "understat_minutes"] + performance_columns
#     ].to_string(index=False)
# )

# print(
#     f"\nPlayers with 0 minutes but positive performance: "
#     f"{len(invalid_zero_minutes)}"
# )

for column in fotmob_numeric_columns:
    invalid = all_candidates_fotmob[
        all_candidates_fotmob[column].notna()
        & (all_candidates_fotmob[column] < 0)
    ]

    # print(f"{column}: {len(invalid)} negative values")
    
    invalid_goals_assists = all_candidates_fotmob[
    all_candidates_fotmob["fotmob_goals"].notna()
    & all_candidates_fotmob["fotmob_assists"].notna()
    & all_candidates_fotmob["goals_and_assists"].notna()
    & (
        (
            all_candidates_fotmob["fotmob_goals"]
            + all_candidates_fotmob["fotmob_assists"]
        )
        != all_candidates_fotmob["goals_and_assists"]
    )
]

# print(
#     invalid_goals_assists[
#         [
#             "player_name",
#             "fotmob_goals",
#             "fotmob_assists",
#             "goals_and_assists"
#         ]
#     ].to_string(index=False)
# )

# print(
#     f"\nGoals + assists mismatches: {len(invalid_goals_assists)}"
# )

fotmob_per90_columns = [
    "goals_per_90",
    "xG_per_90",
    "shots_on_target_per_90",
    "shots_per_90",
    "accurate_passes_per_90",
    "accurate_long_balls_per_90",
    "xA_per_90",
    "xG_and_xA_per_90",
    "successful_dribbles_per_90",
    "defensive_actions_per_90",
    "recoveries_per_90",
    "possession_won_final_3rd_per_90"
]

for column in fotmob_per90_columns:
    invalid = all_candidates_fotmob[
        all_candidates_fotmob["fotmob_minutes"].notna()
        & (all_candidates_fotmob["fotmob_minutes"] == 0)
        & all_candidates_fotmob[column].notna()
        & (all_candidates_fotmob[column] > 0)
    ]

    # print(f"{column}: {len(invalid)} zero-minute violations")
    
    
    minutes_comparison = all_candidates_fotmob[
    all_candidates_fotmob["understat_minutes"].notna()
    & all_candidates_fotmob["fotmob_minutes"].notna()
].copy()

minutes_comparison["minutes_difference"] = (
    minutes_comparison["understat_minutes"]
    - minutes_comparison["fotmob_minutes"]
)

# print(
#     minutes_comparison[
#         [
#             "player_name",
#             "understat_minutes",
#             "fotmob_minutes",
#             "minutes_difference"
#         ]
#     ].sort_values(
#         "minutes_difference",
#         key=lambda x: x.abs(),
#         ascending=False
#     ).to_string(index=False)
# )

# print(
#     all_candidates_fotmob["fotmob_rating"].describe()
# )





checks = {}


mask = (
    all_candidates_fotmob["xG_per_90"].notna()
    & all_candidates_fotmob["xA_per_90"].notna()
    & all_candidates_fotmob["xG_and_xA_per_90"].notna()
)

difference = (
    all_candidates_fotmob.loc[mask, "xG_per_90"]
    + all_candidates_fotmob.loc[mask, "xA_per_90"]
    - all_candidates_fotmob.loc[mask, "xG_and_xA_per_90"]
)

checks["xG + xA per 90 mismatch"] = (difference.abs() > 0.02).sum()



mask = (
    all_candidates_fotmob["fotmob_goals"].notna()
    & all_candidates_fotmob["fotmob_minutes"].notna()
    & all_candidates_fotmob["goals_per_90"].notna()
    & (all_candidates_fotmob["fotmob_minutes"] > 0)
)

calculated = (
    all_candidates_fotmob.loc[mask, "fotmob_goals"]
    / all_candidates_fotmob.loc[mask, "fotmob_minutes"]
    * 90
)

difference = (
    calculated
    - all_candidates_fotmob.loc[mask, "goals_per_90"]
)

checks["Goals per 90 mismatch"] = (difference.abs() > 0.02).sum()



mask = (
    all_candidates_fotmob["fotmob_xG"].notna()
    & all_candidates_fotmob["fotmob_minutes"].notna()
    & all_candidates_fotmob["xG_per_90"].notna()
    & (all_candidates_fotmob["fotmob_minutes"] > 0)
)

calculated = (
    all_candidates_fotmob.loc[mask, "fotmob_xG"]
    / all_candidates_fotmob.loc[mask, "fotmob_minutes"]
    * 90
)

difference = (
    calculated
    - all_candidates_fotmob.loc[mask, "xG_per_90"]
)

checks["xG per 90 mismatch"] = (difference.abs() > 0.02).sum()



mask = (
    all_candidates_fotmob["fotmob_xA"].notna()
    & all_candidates_fotmob["fotmob_minutes"].notna()
    & all_candidates_fotmob["xA_per_90"].notna()
    & (all_candidates_fotmob["fotmob_minutes"] > 0)
)

calculated = (
    all_candidates_fotmob.loc[mask, "fotmob_xA"]
    / all_candidates_fotmob.loc[mask, "fotmob_minutes"]
    * 90
)

difference = (
    calculated
    - all_candidates_fotmob.loc[mask, "xA_per_90"]
)

checks["xA per 90 mismatch"] = (difference.abs() > 0.02).sum()



# for check, failures in checks.items():
#     print(f"{check}: {failures} violations")

validation_columns = [
    "player_name",
    "league",
    "transfermarkt_club",
    "transfermarkt_code",
    "understat_id",
    "understat_minutes",
    "understat_goals",
    "understat_xG",
    "understat_assists",
    "understat_xA",
    "fotmob_id",
    "fotmob_minutes",
    "fotmob_goals",
    "fotmob_xG",
    "fotmob_assists",
    "fotmob_xA",
    "fotmob_rating"
]

missing_report = pd.DataFrame({
    "missing_count": all_candidates_fotmob[validation_columns].isna().sum(),
    "missing_pct": (
        all_candidates_fotmob[validation_columns].isna().mean() * 100
    ).round(1)
})

# print(missing_report.to_string())

fotmob_assists_missing_extra = all_candidates_fotmob[
    all_candidates_fotmob["fotmob_id"].notna()
    & all_candidates_fotmob["fotmob_assists"].isna()
]

print(
    fotmob_assists_missing_extra[
        [
            "player_name",
            "fotmob_id",
            "fotmob_minutes",
            "fotmob_goals",
            "fotmob_xG",
            "fotmob_xA",
            "data_group"
        ]
    ].to_string(index=False)
)

# print(
#     f"\nFotMob ID present but assists missing: "
#     f"{len(fotmob_assists_missing_extra)}"
# )

fotmob_rating_missing_extra = all_candidates_fotmob[
    all_candidates_fotmob["fotmob_id"].notna()
    & all_candidates_fotmob["fotmob_rating"].isna()
]

print(
    fotmob_rating_missing_extra[
        [
            "player_name",
            "fotmob_id",
            "fotmob_minutes",
            "fotmob_goals",
            "fotmob_xG",
            "fotmob_xA",
            "data_group"
        ]
    ].to_string(index=False)
)

# print(
#     f"\nFotMob ID present but rating missing: "
#     f"{len(fotmob_rating_missing_extra)}"
# )

for column in ["transfermarkt_code", "understat_id", "fotmob_id"]:

    duplicate_ids = all_candidates_fotmob[
        all_candidates_fotmob[column].notna()
        & all_candidates_fotmob.duplicated(
            subset=[column],
            keep=False
        )
    ].sort_values(column)

    print(f"\n{column}")
    print("-" * len(column))

    if duplicate_ids.empty:
        print("No duplicate IDs")
    else:
        print(
            duplicate_ids[
                ["player_name", column]
            ].to_string(index=False)
        )

    print(f"Duplicate records: {len(duplicate_ids)}")