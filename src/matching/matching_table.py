import pandas as pd
from matching_player import result_matched_players


players_df=pd.DataFrame(result_matched_players)

players_df["player_key"]=range(1, len(players_df) + 1)

null_fotmob_df=players_df[players_df["fotmob_id"].isna()]

null_understat_df=players_df[players_df["understat_id"].isna()]

not_null_fotmob_df=players_df[players_df["fotmob_id"].notnull()]

not_null_understat_df=players_df[players_df["understat_id"].notnull()]

both_null_df=players_df[players_df["fotmob_id"].isna() & players_df["understat_id"].isna()]

print("Number of Rows where fotmob and understat id is Null : " , len(both_null_df))
print("Number of rows where understat id is not null :" , len(not_null_understat_df))
print("Number of rows where fotmob id is not null : " ,len(not_null_fotmob_df))
print("Number of rows where fotmob id is null :" ,len(null_fotmob_df))
print("Number of rows where understat id is null :" ,len(null_understat_df))


