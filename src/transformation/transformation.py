import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from loading.loading_fotmob import all_candidates_fotmob

all_candidates_fotmob = all_candidates_fotmob.rename(
    columns={
        "transfermarkt_code":"transfermarkt_id",
        "transfermarkt_club":"club_2025_26",
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

all_candidates_fotmob["date_of_birth"] = pd.to_datetime(
    all_candidates_fotmob["date_of_birth"],
    format="%d/%m/%Y",
    errors="coerce"
)
# print(all_candidates_fotmob["date_of_birth"][0])        
# print(type(date_object)) 

# print(all_candidates_fotmob.columns.tolist())
# print(all_candidates_fotmob.shape)
# print(all_candidates_fotmob.head())