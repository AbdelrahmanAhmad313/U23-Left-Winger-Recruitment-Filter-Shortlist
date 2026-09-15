import sys
from pathlib import Path
import pandas as pd
sys.path.append(str(Path(__file__).resolve().parents[1]))

from transformation.transformation import all_candidates_fotmob


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


club_corrections = {
    "1.FC K�ln": "1.FC Köln",
    "Borussia M�nchengladbach": "Borussia Mönchengladbach",
    "Deportivo Alav�s": "Deportivo Alavés"
}

all_candidates_fotmob["club_2025_26"] = (
    all_candidates_fotmob["club_2025_26"].replace(club_corrections)
)


all_candidates_fotmob["current_club"] = (
    all_candidates_fotmob["current_club"]
    .apply(lambda x: x["href"].split("/")[1])
    .str.replace("-"," ")
)
all_candidates_fotmob["contract_expires"] = pd.to_datetime(
    all_candidates_fotmob["contract_expires"].replace("-", pd.NaT),
    format="%d/%m/%Y",
    errors="coerce"
)
all_candidates_fotmob["foot"]=(
    all_candidates_fotmob["foot"].fillna("No Info")
)




reference_date = pd.Timestamp("2026-07-01")

all_candidates_fotmob["age_2026_07_01"] = (
    reference_date.year
    - all_candidates_fotmob["date_of_birth"].dt.year
    - (
        (all_candidates_fotmob["date_of_birth"].dt.month > reference_date.month)
        |
        (
            (all_candidates_fotmob["date_of_birth"].dt.month == reference_date.month)
            &
            (all_candidates_fotmob["date_of_birth"].dt.day > reference_date.day)
        )
    ).astype(int)
)

# print(all_candidates_fotmob.columns)
# print(all_candidates_fotmob[["player_key","age_2026_07_01","current_club","date_of_birth","position","contract_expires","current_market_value","foot"]])