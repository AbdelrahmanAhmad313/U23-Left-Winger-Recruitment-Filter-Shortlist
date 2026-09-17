import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from validation.validation import all_candidates,player_valuations_df
from matching.matching_player import PROJECT_ROOT

candidate_players_columns = [
    "player_key",
"player_name",
"league",
"club_2025_26",
"date_of_birth",
"age_2026_07_01",
"position",
"foot",
"contract_expires",
"current_club",
]

market_value_columns=[
    "player_key",
    "valuation_date",
    "market_value_in_eur"
]

source_identity_columns = [
    "player_key",
"transfermarkt_id",
"understat_id",
"fotmob_id",
]

understat_stats_columns = [
   "player_key",
"understat_games",
"understat_minutes",
"understat_goals",
"understat_xG",
"understat_assists",
"understat_xA",
"understat_shots",
"understat_key_passes",
"understat_npxG",
]

fotmob_stats_columns = [
    "player_key",
   'fotmob_goals',
    'fotmob_assists',
    'goals_and_assists', 
    'fotmob_rating',
    'fotmob_minutes',
    'goals_per_90', 
    'fotmob_xG',
    'xG_per_90', 
    'xGOT',
    'shots_on_target_per_90', 
    'shots_per_90', 
    'accurate_passes_per_90',
    'big_chances_created',
    'chances_created',
    'accurate_long_balls_per_90',
    'fotmob_xA', 'xA_per_90',
    'xG_and_xA_per_90',
    'successful_dribbles_per_90',
    'big_chances_missed',
    'defensive_actions_per_90', 
    'recoveries_per_90',
    'possession_won_final_3rd_per_90',
    
]

candidate_data_status_columns = [
    "player_key",
"data_group",
"data_status",
]

candidate_players_df=all_candidates[candidate_players_columns]
source_identity_df=all_candidates[source_identity_columns]
understat_stats_df=all_candidates.loc[all_candidates["understat_id"].notna(),understat_stats_columns]
fotmob_stats_df=all_candidates.loc[all_candidates["fotmob_id"].notna(),fotmob_stats_columns]
candidate_data_status_df=all_candidates[candidate_data_status_columns]
market_value_df=player_valuations_df[market_value_columns]



# =========================
# MODEL VALIDATION
# =========================

assert candidate_players_df["player_key"].is_unique
assert source_identity_df["player_key"].is_unique
assert understat_stats_df["player_key"].is_unique
assert fotmob_stats_df["player_key"].is_unique
assert candidate_data_status_df["player_key"].is_unique

assert understat_stats_df["player_key"].isin(
    candidate_players_df["player_key"]
).all()

assert fotmob_stats_df["player_key"].isin(
    candidate_players_df["player_key"]
).all()

assert source_identity_df["player_key"].isin(
    candidate_players_df["player_key"]
).all()

assert candidate_data_status_df["player_key"].isin(
    candidate_players_df["player_key"]
).all()

print("Model validation passed.")


# =========================
# EXPORT MODEL TABLES
# =========================

MODEL_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "model"
)

MODEL_DIR.mkdir(parents=True, exist_ok=True)

candidate_players_df.to_csv(
    MODEL_DIR / "candidate_players.csv",
    index=False
)

source_identity_df.to_csv(
    MODEL_DIR / "source_identity.csv",
    index=False
)

understat_stats_df.to_csv(
    MODEL_DIR / "understat_stats.csv",
    index=False
)

fotmob_stats_df.to_csv(
    MODEL_DIR / "fotmob_stats.csv",
    index=False
)

candidate_data_status_df.to_csv(
    MODEL_DIR / "candidate_data_status.csv",
    index=False
)

player_valuations_df.to_csv(
    MODEL_DIR / "market_value.csv",
    index=False
)

print("Model tables exported successfully.")

# =========================
# FINAL MODEL SUMMARY
# =========================

print("\nFinal model summary:")
print("candidate_players:", candidate_players_df.shape)
print("source_identity:", source_identity_df.shape)
print("understat_stats:", understat_stats_df.shape)
print("fotmob_stats:", fotmob_stats_df.shape)
print("candidate_data_status:", candidate_data_status_df.shape)

print("\nUnique player counts:")
print(
    "candidate_players:",
    candidate_players_df["player_key"].nunique()
)
print(
    "source_identity:",
    source_identity_df["player_key"].nunique()
)
print(
    "understat_stats:",
    understat_stats_df["player_key"].nunique()
)
print(
    "fotmob_stats:",
    fotmob_stats_df["player_key"].nunique()
)
print(
    "candidate_data_status:",
    candidate_data_status_df["player_key"].nunique()
)


