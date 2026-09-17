import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from validation.validation import all_candidates

# How many candidates do we actually have, 
# and how many have enough Understat minutes for reliable performance analysis and their league?

# print("Number of candidates :",len(all_candidates))
# print("Number of candidate with understat stats :",len(all_candidates[all_candidates["understat_id"].notnull()]))
# print("Number of candidates with more than or equal 900 understat minutes :",
#       len(all_candidates[all_candidates["understat_minutes"]>=900]))
# print("Number of candidates with less 900 understat minutes :",
#       len(all_candidates[all_candidates["understat_minutes"]<900]))

# print("Number of candidates with more than or equal 900 understat minutes in the laliga is :",len(all_candidates[(all_candidates["league"]=="LaLiga") & (all_candidates["understat_minutes"]>=900)]))

# print("Number of candidates with more than or equal 900 understat minutes in the bundeliga is :",len(all_candidates[(all_candidates["league"]=="Bundesliga" )& (all_candidates["understat_minutes"]>=900)]))


# How spread out is attacking production among our reliable-performance population?

eligible_playtime_candidates=all_candidates[all_candidates["understat_minutes"]>=900]

# print(eligible_playtime_candidates["understat_xG"].describe())
# print(eligible_playtime_candidates["understat_xA"].describe())
# print(eligible_playtime_candidates["understat_minutes"].describe())


# Does the picture change when we normalize attacking output by playing time?

eligible_playtime_candidates["xG_per_90"]=(eligible_playtime_candidates["understat_xG"]/eligible_playtime_candidates["understat_minutes"])*90

eligible_playtime_candidates["xA_per_90"]=(eligible_playtime_candidates["understat_xA"]/eligible_playtime_candidates["understat_minutes"])*90
eligible_playtime_candidates["expected_contribution_per_90"]= eligible_playtime_candidates["xG_per_90"]+eligible_playtime_candidates["xA_per_90"]

# print(eligible_playtime_candidates["xG_per_90"].describe())
# print(eligible_playtime_candidates["xA_per_90"].describe())
# print(eligible_playtime_candidates["expected_contribution_per_90"].describe())

# What does the distribution actually look like at player level?

# print(eligible_playtime_candidates[["player_name","league","understat_minutes","xG_per_90","xA_per_90","expected_contribution_per_90"]].sort_values("expected_contribution_per_90",ascending=False))

# Outlier detection

eligible_playtime_candidates["xG_per_90_z"]=(eligible_playtime_candidates["xG_per_90"]-eligible_playtime_candidates["xG_per_90"].mean())/eligible_playtime_candidates["xG_per_90"].std()
# print(eligible_playtime_candidates[["player_name","xG_per_90","xG_per_90_z"]].sort_values("xG_per_90_z", ascending=False))

# Does a player who generates more expected goals per 90 also tend to generate more expected assists per 90?

# print("XG per 90 Correlation to XA per 90 :",eligible_playtime_candidates["xG_per_90"].corr(
#     eligible_playtime_candidates["xA_per_90"]
# ).__round__(3))


# 
