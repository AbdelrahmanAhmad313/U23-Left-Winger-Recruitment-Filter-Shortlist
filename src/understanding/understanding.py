import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from loading.loading_fotmob import all_candidates_fotmob

id_columns = all_candidates_fotmob[
    [
        "player_key",
        "player_name",
        "fotmob_id",
        "fotmob_name",
        "participant_id"
    ]
]

missing = all_candidates_fotmob.isna().sum()

# print(
#     missing[
#         missing > 0
#     ].sort_values(ascending=False)
# )

missing_pct = (
    all_candidates_fotmob.isna().mean() * 100
).sort_values(ascending=False)

# print(
#     missing_pct[
#         missing_pct > 0
#     ]
# )

# print(
#     all_candidates_fotmob[
#         all_candidates_fotmob["fotmob_id"].notna()
#         & all_candidates_fotmob["fotmob_rating"].isna()
#     ][
#         [
#             "player_key",
#             "player_name",
#             "league",
#             "fotmob_id",
#             "participant_id",
#             "minutes_y",
#         ]
#     ].to_string(index=False)
# )

# print(
#     all_candidates_fotmob[
#         [
#             "games",
#             "minutes_x",
#             "goals_x",
#             "xG_x",
#             "assists_x",
#             "xA_x",
#             "shots",
#             "key_passes",
#             "npxG"
#         ]
#     ].describe()
# )

# print(
#     all_candidates_fotmob[
#         [
#             "player_name",
#             "games",
#             "minutes_x",
#             "goals_x",
#             "xG_x",
#             "assists_x",
#             "xA_x"
#         ]
#     ].head(15).to_string(index=False)
# )

comparison = all_candidates_fotmob[
    all_candidates_fotmob["data_group"] == "Both"
][
    [
        "player_name",
        "understat_id",
        "fotmob_id",
        "goals_x",
        "goals_y",
        "xG_x",
        "xG_y",
        "assists_x",
        "assists_y",
        "xA_x",
        "xA_y",
        "minutes_x",
        "minutes_y"
    ]
]

# print(comparison.to_string(index=False))

# print("Rows:", len(all_candidates_fotmob))
# print("Unique player keys:", all_candidates_fotmob["player_key"].nunique())
# print("Duplicate player keys:", all_candidates_fotmob["player_key"].duplicated().sum())