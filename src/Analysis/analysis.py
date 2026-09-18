import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from validation.validation import all_candidates
from cleaning.cleaning import player_valuations_df

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


# compare the two leagues in our actual sample.
# print(eligible_playtime_candidates.groupby("league").agg({"understat_xG":"mean","understat_xA":"mean","expected_contribution_per_90":["mean","median"]}))


# Compare attacking output distribution (xG/90 and xA/90) by league

# print(eligible_playtime_candidates.groupby("league").agg({"xG_per_90":["mean","median","std"],"xA_per_90":["mean","median","std"]}))


# Attacking Profile
avg_xG_per_90=eligible_playtime_candidates["xG_per_90"].mean()
avg_xA_per_90=eligible_playtime_candidates["xA_per_90"].mean()
for index, player in eligible_playtime_candidates.iterrows():

    if (
        player["xG_per_90"] > avg_xG_per_90
        and player["xA_per_90"] > avg_xA_per_90
    ):
        profile = "Goal Threat & Creator"

    elif player["xG_per_90"] > avg_xG_per_90:
        profile = "Goal Threat"

    elif player["xA_per_90"] > avg_xA_per_90:
        profile = "Creator"

    else:
        profile = "Below Average"

    eligible_playtime_candidates.loc[index, "profile"] = profile
        
# print(
#     eligible_playtime_candidates[
#         ["player_name", "xG_per_90", "xA_per_90","expected_contribution_per_90", "profile"]
#     ].sort_values(
#         "expected_contribution_per_90",
#         ascending=False
#     ).drop(columns=['expected_contribution_per_90'])
# )

# Analyze attacking profile distribution


# print(eligible_playtime_candidates.groupby("profile").size())

# Analyze attacking profiles across leagues


# print(eligible_playtime_candidates.pivot_table(index="profile",columns="league",aggfunc="size",fill_value=0))


# Assess FotMob coverage for dribbling and chance creation

# print("players with successful_dribbles_per_90 :",eligible_playtime_candidates["successful_dribbles_per_90"].notna().sum())
# print("players with chances_created :",eligible_playtime_candidates["chances_created"].notna().sum())
# print("players with both :",eligible_playtime_candidates[["successful_dribbles_per_90","chances_created"]].notna().all(axis=1).sum())


# Chances created per 90(fotmob)

eligible_playtime_candidates["chances_created_per_90"]=(eligible_playtime_candidates["chances_created"]/eligible_playtime_candidates["fotmob_minutes"])*90.0

# print(eligible_playtime_candidates["chances_created_per_90"])

# Which players demonstrate different types of attacking value?


candidates_attacking_table=eligible_playtime_candidates[["player_name","league",
                                                         "understat_minutes",
                                                         "xG_per_90",
                                                         "xA_per_90",
                                                         "expected_contribution_per_90",
                                                         "successful_dribbles_per_90",
                                                         "chances_created_per_90",
                                                         "profile"]]

# print(candidates_attacking_table.sort_values("expected_contribution_per_90",ascending=False))


# Which candidates contribute across multiple attacking dimensions rather than relying heavily on one?
# Measure attacking balance across scoring and chance creation


eligible_playtime_candidates["attacking_balance"]=eligible_playtime_candidates[['xG_per_90', 'xA_per_90']].min(axis=1)
# print(eligible_playtime_candidates[["player_name",
#                                     "xG_per_90",
#                                     "xA_per_90",
#                                     "expected_contribution_per_90",
#                                     "attacking_balance"]]
#       .sort_values("attacking_balance",ascending=False))


# Measure player attacking output relative to the candidate population


eligible_playtime_candidates["xG_difference_from_avg"]=eligible_playtime_candidates["xG_per_90"]-(eligible_playtime_candidates["xG_per_90"].mean())
eligible_playtime_candidates["xA_difference_from_avg"]=eligible_playtime_candidates["xA_per_90"]-(eligible_playtime_candidates["xA_per_90"].mean())
# print(eligible_playtime_candidates[["player_name",
#                                     "xG_difference_from_avg",
#                                     "xA_difference_from_avg",
#                                     "attacking_balance",
#                                     "expected_contribution_per_90"]].sort_values("expected_contribution_per_90",ascending=False))


# Classify players by relative scoring and creation profile



for index, player in eligible_playtime_candidates.iterrows():

    if (player["xG_difference_from_avg"]>=0 and
     player["xA_difference_from_avg"]>=0
     ):
        attacking_archetype ="All-Round Attacker"
    
    elif(player["xG_difference_from_avg"]>0
         and player["xA_difference_from_avg"]<0
     ):
      attacking_archetype="Goal-Focused Attacker"
         
    elif(player["xG_difference_from_avg"]<0 and
         player["xA_difference_from_avg"]>0):
        
             attacking_archetype ="Creator"
    else:
        attacking_archetype ="Below Population Average"
        
    eligible_playtime_candidates.loc[index, "attacking_archetype"] = attacking_archetype
        
# print(eligible_playtime_candidates[["player_name","xG_difference_from_avg","xA_difference_from_avg","attacking_archetype"]])
         
        
# Analyze dribbling and chance creation distribution

# print(eligible_playtime_candidates["successful_dribbles_per_90"].describe())
# print(eligible_playtime_candidates["chances_created_per_90"].describe())
    
# Measure dribbling and chance creation relative to the candidate population

eligible_playtime_candidates["successful_dribbles_difference_from_avg"]=eligible_playtime_candidates["successful_dribbles_per_90"]-(eligible_playtime_candidates["successful_dribbles_per_90"].mean())
eligible_playtime_candidates["chances_created_difference_from_avg"]=eligible_playtime_candidates["chances_created_per_90"]-(eligible_playtime_candidates["chances_created_per_90"].mean())

# print(eligible_playtime_candidates[["player_name","successful_dribbles_per_90",
#                                     "successful_dribbles_difference_from_avg",
#                                     "chances_created_per_90",
#                                     "chances_created_difference_from_avg"]])


# Classify players by 1v1 and chance creation profile

for index, player in eligible_playtime_candidates.iterrows():

    if (player["successful_dribbles_difference_from_avg"]>=0 and
     player["chances_created_difference_from_avg"]>=0
     ):
        wide_attacking_archetype ="Ball-Carrying Creator"
    
    elif(player["successful_dribbles_difference_from_avg"]>0
         and player["chances_created_difference_from_avg"]<0
     ):
      wide_attacking_archetype="Direct Ball Carrier"
         
    elif(player["successful_dribbles_difference_from_avg"]<0 and
         player["chances_created_difference_from_avg"]>0):
        
             wide_attacking_archetype ="Creative Facilitator"
    else:
        wide_attacking_archetype ="Lower 1v1 & Creation Output"
        
    eligible_playtime_candidates.loc[index, "wide_attacking_archetype"] = wide_attacking_archetype
    
# print(eligible_playtime_candidates[["player_name","successful_dribbles_per_90","chances_created_per_90","wide_attacking_archetype"]])



# Combine attacking output and wide-attacking profile

# print(eligible_playtime_candidates[["player_name","attacking_archetype",
#                                     "wide_attacking_archetype",
#                                     "expected_contribution_per_90",
#                                     "attacking_balance"]])

# Add age, contract, club and market-value context to the attacking profiles



recruitment_candidates_df=eligible_playtime_candidates.merge(
    player_valuations_df,
    on="player_key",
    how="inner"
)

# print(candidates_evaluation[["player_name",
#                                    "league",
#                                    "age_2026_07_01",
#                                    "understat_minutes",
#                                    "contract_expires",
#                                    "current_club",
#                                    "market_value_in_eur"]])

# Classify contract accessibility within the recruitment window

for index,player in recruitment_candidates_df.iterrows():
    if player["contract_expires"]<=(pd.to_datetime("2028-07-01")):
        contract_window="Within 24 Months"
    else:
        contract_window="Beyond 24 Months"
    
    recruitment_candidates_df.loc[index,"contract_window"]= contract_window
    
    
# print(recruitment_candidates_df[["player_name","contract_expires","contract_window","market_value_in_eur"]])


# Build player-level recruitment context

# print(recruitment_candidates_df[["player_name",
#                                  "attacking_archetype",
#                                  "wide_attacking_archetype",
#                                  "age_2026_07_01",
#                                  "understat_minutes",
#                                  "expected_contribution_per_90",
#                                  "attacking_balance",
#                                  "contract_window",
#                                  "market_value_in_eur",
#                                  ]])


# Analyze defensive contribution distribution

# print(recruitment_candidates_df["defensive_actions_per_90"].describe())
# print(recruitment_candidates_df["recoveries_per_90"].describe())
# print(recruitment_candidates_df["possession_won_final_3rd_per_90"].describe())

# Measure defensive contribution relative to the candidate population


recruitment_candidates_df["defensive_actions_difference_per_90_from_avg"]=recruitment_candidates_df["defensive_actions_per_90"]-recruitment_candidates_df["defensive_actions_per_90"].mean()
recruitment_candidates_df["recoveries_difference_per_90_from_avg"]=recruitment_candidates_df["recoveries_per_90"]-recruitment_candidates_df["recoveries_per_90"].mean()
recruitment_candidates_df["final_third_wins_difference_per_90_from_avg"]=recruitment_candidates_df["possession_won_final_3rd_per_90"]-recruitment_candidates_df["possession_won_final_3rd_per_90"].mean()

# print(recruitment_candidates_df[["player_name",
#                                  "defensive_actions_per_90",
#                                  "defensive_actions_difference_per_90_from_avg",
#                                  "recoveries_per_90",
#                                  "recoveries_difference_per_90_from_avg",
#                                  "possession_won_final_3rd_per_90",
#                                  "final_third_wins_difference_per_90_from_avg",]])


# Classify players by defensive involvement and final-third possession wins

for index,player in recruitment_candidates_df.iterrows():
    if (player["defensive_actions_difference_per_90_from_avg"]>=0 and
         player["final_third_wins_difference_per_90_from_avg"]>=0
         ):
            defensive_profile ="Active High Press Contributor"
        
    elif(player["defensive_actions_difference_per_90_from_avg"]>0
             and player["final_third_wins_difference_per_90_from_avg"]<0
         ):
          defensive_profile="Defensively Active"
             
    elif(player["defensive_actions_difference_per_90_from_avg"]<0 and
             player["final_third_wins_difference_per_90_from_avg"]>0):
            
            defensive_profile ="High Final-Third Recovery"
    else:
            defensive_profile ="Lower Defensive Output"
    
    recruitment_candidates_df.loc[index,"defensive_profile"]= defensive_profile
    
    
# print(recruitment_candidates_df[["player_name",
#                                  "defensive_actions_per_90",
#                                  "possession_won_final_3rd_per_90",
#                                  "defensive_profile",]])



# Build the final multi-dimensional candidate analysis view


# print(recruitment_candidates_df[["player_name",
#                                  "league",
#                                  "age_2026_07_01",
#                                  "understat_minutes",
#                                  "expected_contribution_per_90",
#                                  "attacking_balance",
#                                  "attacking_archetype",
#                                  "successful_dribbles_per_90",
#                                  "chances_created_per_90",
#                                  "wide_attacking_archetype",
#                                  "defensive_actions_per_90",
#                                  "possession_won_final_3rd_per_90",
#                                  "defensive_profile",
#                                  "contract_window",
#                                  "market_value_in_eur",]].sort_values("expected_contribution_per_90",ascending=False))


# Document limitations of the Python recruitment analysis

limitations = [
    "The analysis does not capture the player's tactical role or exact positional usage.",
    "The available data does not provide enough information to evaluate pressing quality, only observable defensive contribution metrics.",
    "The analysis cannot determine whether a player's performance is sustainable over multiple seasons.",
    "The analysis does not account for team strength, possession, teammates, or tactical context.",
    "The analysis cannot determine injury history, physical condition, or future availability.",
    "Market value is an estimated valuation and does not represent the actual transfer fee or total acquisition cost.",
    "The analysis cannot determine whether a player would adapt successfully to a different league, club, or tactical system."
]
