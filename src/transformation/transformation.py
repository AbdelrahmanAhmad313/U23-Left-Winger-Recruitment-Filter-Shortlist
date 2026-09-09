import pandas as pd

final_df=[]
data_path="data/raw/"
fotmob_df = pd.read_json(f"{data_path}fotmob/bundesliga_2025_26/Goals.json")
transfermarket_df=pd.read_json(f"{data_path}transfermarkt-scraper/bundesliga_u23_left_wingers_2025_26.json",
                               encoding="cp1252",
                               lines=True,)

top_scorer = fotmob_df["TopLists"][0]

top_scorers_df = pd.DataFrame(top_scorer["StatList"])
statsNameCapital= top_scorer["StatName"].capitalize()
top_scorers_df=top_scorers_df.rename(
    columns={
        "ParticiantId":"Player Id",
        "ParticipantName":"Player Name",
        "TeamId":"Team Id",
        "TeamName":"Team Name",
        "StatValue":statsNameCapital,
    }
)
# print(top_scorers_df[["Player Id","Player Name","Team Id","Team Name",statsNameCapital]])
# print(top_scorers_df[top_scorers_df["Player Name"]=="justin diehl"])

# final_df=transfermarket_df.merge(
#     how="left",
#     on=transfermarket_df[""]
    
# )
# print(transfermarket_df.columns)


# justin-diehl--> transfermarket
#

import difflib
from difflib import SequenceMatcher

# Find closest matches in a list

names = top_scorers_df["Player Name"].tolist()

closest = difflib.get_close_matches(
    "Justin ",
    names,
    n=5,
    cutoff=0.6
)

print(closest) # Output: ['apple', 'appeal']

# # Get a percentage score (0.0 to 1.0) between two strings
# score = SequenceMatcher(None, "apple", "appeal").ratio()
# print(score)  # Output: 0.7272727272727273
