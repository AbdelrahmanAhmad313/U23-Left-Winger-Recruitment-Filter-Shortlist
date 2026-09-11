import pandas as pd
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FOTMOB_BUNDESLIGA_GOALS_PATH=(
    PROJECT_ROOT    
    / "data"
    / "raw"
    / "fotmob"
    /"bundesliga_2025_26"
    / "Goals.json"
)

def fotmobPath(league,metric):
    fotmob_data_path=(
    PROJECT_ROOT
    /"data"
    /"raw"
    /"fotmob"
    /f"{league}_2025_26"
    /f"{metric}.json"
)

    return fotmob_data_path


def load_fotmob(path):
    """Load an Fotmob JSON array."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    players = []

    for top_list in data["TopLists"]:
        players.extend(top_list["StatList"])

    return players




fotmob_goals_df = pd.DataFrame(load_fotmob(fotmobPath("bundesliga","Goals")))
fotmob_xg_df = pd.DataFrame(load_fotmob(fotmobPath("bundesliga","xG")))

# transfermarket_df=pd.read_json(f"{data_path}transfermarkt-scraper/bundesliga_u23_left_wingers_2025_26.json",
#                                encoding="cp1252",
#                                lines=True,)


fotmob_goals_df = fotmob_goals_df[
    ["ParticiantId", "ParticipantName", "TeamName", "StatValue"]
].rename(
    columns={"StatValue": "goals"}
)

fotmob_xg_df = fotmob_xg_df[
    ["ParticiantId", "StatValue"]
].rename(
    columns={"StatValue": "xG"}
)

all_fotmob_players = fotmob_goals_df.merge(
    fotmob_xg_df,
    on="ParticiantId",
    how="outer"
)
all_fotmob_players = all_fotmob_players.rename(
    columns={"ParticiantId": "participant_id"}
)

# print(all_fotmob_players.shape)
# print(all_fotmob_players.head())
# print(all_fotmob_players.columns.tolist())
# print(all_fotmob_players)