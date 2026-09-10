import pandas as pd
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
    / "Assists.json"
)

def load_fotmob(path):
    """Load an Fotmob JSON array."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    players = []

    for top_list in data["TopLists"]:
        players.extend(top_list["StatList"])

    return players


fotmob_df=pd.DataFrame(load_fotmob(FOTMOB_BUNDESLIGA_PATH))

print(fotmob_df[fotmob_df["TeamName"].str.contains('Stu')])

# Justin Diehl  