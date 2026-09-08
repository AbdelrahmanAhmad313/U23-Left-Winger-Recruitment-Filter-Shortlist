import pandas as pd 

df= pd.read_json("data/raw/fotmob/bundesliga_2025_26/Goals.json")

top_scorer_df=pd.DataFrame.from_dict(df)

top_scorer = top_scorer_df["TopLists"]
print(top_scorer["StatList"])

# for scorer in top_scorer["StatList"]:
#     result.append(scorer["ParticipantName"])




