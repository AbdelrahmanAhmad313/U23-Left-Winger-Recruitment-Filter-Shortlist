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

high_xg_threshold = eligible_playtime_candidates["xG_per_90"].quantile(0.65)

acceptable_xg_threshold = eligible_playtime_candidates["xG_per_90"].quantile(0.40)

high_xa_threshold = eligible_playtime_candidates["xA_per_90"].quantile(0.65)

acceptable_xa_threshold = eligible_playtime_candidates["xA_per_90"].quantile(0.40)

# -----

dribble_threshold = eligible_playtime_candidates["successful_dribbles_per_90"].quantile(0.45)

defensive_threshold = eligible_playtime_candidates["defensive_actions_per_90"].quantile(0.35)

recovery_threshold = eligible_playtime_candidates["recoveries_per_90"].quantile(0.35)

pressing_threshold = eligible_playtime_candidates["possession_won_final_3rd_per_90"].quantile(0.40)

# print((
#     (eligible_playtime_candidates["xG_per_90"] >= xg_threshold) &
#     (eligible_playtime_candidates["xA_per_90"] >= xa_threshold) 
    # &
    # (eligible_playtime_candidates["successful_dribbles_per_90"] >= dribble_threshold) &
    # (eligible_playtime_candidates["defensive_actions_per_90"] >= defensive_threshold) &
    # (eligible_playtime_candidates["recoveries_per_90"] >= recovery_threshold) &
    # (eligible_playtime_candidates["possession_won_final_3rd_per_90"] >= pressing_threshold)
# ).sum())

# print("xG:", xg_threshold)
# print("xA:", xa_threshold)
# print("Dribbles:", dribble_threshold)
# print("Defensive:", defensive_threshold)
# print("Recoveries:", recovery_threshold)
# print("Pressing:", pressing_threshold)

# print("xG:", (
#     eligible_playtime_candidates["xG_per_90"] >= xg_threshold
# ).sum())

# print("xA:", (
#     eligible_playtime_candidates["xA_per_90"] >= xa_threshold
# ).sum())

# print("Dribbles:", (
#     eligible_playtime_candidates["successful_dribbles_per_90"] >= dribble_threshold
# ).sum())

# print("Defensive:", (
#     eligible_playtime_candidates["defensive_actions_per_90"] >= defensive_threshold
# ).sum())

# print("Recoveries:", (
#     eligible_playtime_candidates["recoveries_per_90"] >= recovery_threshold
# ).sum())

# print("Pressing:", (
#     eligible_playtime_candidates["possession_won_final_3rd_per_90"] >= pressing_threshold
# ).sum())

# print(eligible_playtime_candidates.loc[
#     (
#         (eligible_playtime_candidates["xG_per_90"] >= xg_threshold) &
#         (eligible_playtime_candidates["xA_per_90"] >= xa_threshold) &
#         (eligible_playtime_candidates["successful_dribbles_per_90"] >= dribble_threshold) &
#         (eligible_playtime_candidates["defensive_actions_per_90"] >= defensive_threshold) &
#         (eligible_playtime_candidates["recoveries_per_90"] >= recovery_threshold) &
#         (eligible_playtime_candidates["possession_won_final_3rd_per_90"] >= pressing_threshold)
#     ),
#     ["player_name", "xG_per_90", "xA_per_90",
#      "successful_dribbles_per_90", "defensive_actions_per_90",
#      "recoveries_per_90", "possession_won_final_3rd_per_90"]
# ])


for index, player in eligible_playtime_candidates.iterrows():

    # 1. High xG + High xA
    if (
        player["xG_per_90"] >= high_xg_threshold
        and player["xA_per_90"] >= high_xa_threshold
    ):
        profile = "All-Round Attacker"

    # 2. High xG + Acceptable xA
    elif (
        player["xG_per_90"] >= high_xg_threshold
        and player["xA_per_90"] >= acceptable_xa_threshold
        and player["xA_per_90"] < high_xa_threshold
    ):
        profile = "Goal-Focused Attacker"

    # 3. High xG + Low xA
    elif (
        player["xG_per_90"] >= high_xg_threshold
        and player["xA_per_90"] < acceptable_xa_threshold
    ):
        profile = "Goal-Focused / Low Creation"

    # 4. Acceptable xG + High xA
    elif (
        player["xG_per_90"] >= acceptable_xg_threshold
        and player["xG_per_90"] < high_xg_threshold
        and player["xA_per_90"] >= high_xa_threshold
    ):
        profile = "Creator"

    # 5. Acceptable xG + Acceptable xA
    elif (
        player["xG_per_90"] >= acceptable_xg_threshold
        and player["xG_per_90"] < high_xg_threshold
        and player["xA_per_90"] >= acceptable_xa_threshold
        and player["xA_per_90"] < high_xa_threshold
    ):
        profile = "Balanced Attacker"

    # 6. Acceptable xG + Low xA
    elif (
        player["xG_per_90"] >= acceptable_xg_threshold
        and player["xG_per_90"] < high_xg_threshold
        and player["xA_per_90"] < acceptable_xa_threshold
    ):
        profile = "Goal-Focused / Low Creation"

    # 7. Low xG + High xA
    elif (
        player["xG_per_90"] < acceptable_xg_threshold
        and player["xA_per_90"] >= high_xa_threshold
    ):
        profile = "Creator / Low Goal Threat"

    # 8. Low xG + Acceptable xA
    elif (
    player["xG_per_90"] < acceptable_xg_threshold
    and player["xA_per_90"] >= acceptable_xa_threshold
    and player["xA_per_90"] < high_xa_threshold
        ):
        profile = "Creator / Low Goal Threat"

    else:
        profile = "Lower Attacking Output"

    eligible_playtime_candidates.loc[index, "profile"] = profile
    

candidates_attacking_table["profile"]=eligible_playtime_candidates["profile"]

# print(eligible_playtime_candidates[["player_name","profile"]])


for index, player in eligible_playtime_candidates.iterrows():
    
    eligible_playtime_candidates.loc[index,"Meets_goal_threat_threshold"]=player["xG_per_90"]>=high_xg_threshold
    eligible_playtime_candidates.loc[index,"Meets_chance_creation_threshold"]=player["xA_per_90"]>=high_xa_threshold
    eligible_playtime_candidates.loc[index,"Meets_1v1_threshold"]=player["successful_dribbles_per_90"]>=dribble_threshold
    eligible_playtime_candidates.loc[index,"Meets_defensive_actions_baseline"]=player["defensive_actions_per_90"]>=defensive_threshold
    eligible_playtime_candidates.loc[index,"Meets_recoveries_baseline"]=player["recoveries_per_90"]>=recovery_threshold
    eligible_playtime_candidates.loc[index,"Meets_pressing_baseline"]=player["possession_won_final_3rd_per_90"]>=pressing_threshold
    
    
eligible_playtime_candidates=eligible_playtime_candidates.merge(
    player_valuations_df,
    on="player_key",
    how="inner"
)
# print(eligible_playtime_candidates[["player_name",
#                                     "market_value_in_eur",
#                                     "current_club",
#                                     "understat_minutes",
#                                     "fotmob_minutes",
#                                     "contract_expires",
#                                     "age_2026_07_01"]].to_string())


candidate_investigation_summary = {

    "Candidate": [
        "Nusa",
        "El_Mala",
        "Ibrahimovic",
        "Roca",
        "Moleiro"
    ],

    "Attacking_Identity": [
        "Creator-oriented LW",
        "Goal-focused LW",
        "Creator",
        "Goal-focused / low creation",
        "Creator / low goal threat"
    ],

    "Main_Strength": [
        "1v1 + chance creation",
        "Inside movement + goal threat",
        "Passing + chance creation",
        "Goal-focused movement",
        "Movement + passing"
    ],

    "Goal_Threat": [
        "Lower",
        "High",
        "Lower",
        "High",
        "Lower"
    ],

    "Chance_Creation": [
        "Wide creation",
        "Crosses + forward passes",
        "Passing + crosses + set pieces",
        "Direct passes + crosses",
        "Movement + passing"
    ],

    "1v1_Approach": [
        "Strong supporting weapon",
        "Speed + ball control",
        "Passing over 1v1",
        "Meets threshold; not always direct",
        "Positioning over 1v1"
    ],

    "Defensive_Contribution": [
        "High positioning + pressing + recoveries",
        "Limited defensive involvement",
        "High pressing + lane disruption",
        "Tracks back + supports fullback",
        "Pressing + interceptions"
    ],

    "Transition_Behavior": [
        "Wide pressing + attacking transitions",
        "Pace + runs into space",
        "Pressing from advanced areas",
        "Attacks wide space + tracks back",
        "Open-space movement + defensive recovery"
    ],

    "Tactical_Flexibility": [
        "Structure-dependent",
        "Can contribute outside transition situations",
        "Central + wide flexibility",
        "Different attacking + defensive solutions",
        "Multiple attacking + defensive positions"
    ],

    "Main_Concern": [
        "Goal threat + system transferability",
        "Defensive contribution + settled defenses",
        "Goal threat + limited 1v1",
        "Chance creation + pressing",
        "Goal threat + 1v1"
    ],

    "Recruitment_Question": [
        "Can his strengths transfer outside Leipzig's structure?",
        "Can contribute against more settled defensive situations",
        "Can his creativity translate to a higher goal-threat system?",
        "Can he maintain goal threat with less transition space?",
        "Can his creation profile translate to our attacking structure?"
    ]
}
candidate_investigation_summary=pd.DataFrame(candidate_investigation_summary)

candidate_uncertainty_summary = {

    "Candidate": [
        "Nusa",
        "El_Mala",
        "Ibrahimovic",
        "Roca",
        "Moleiro"
    ],

    "Known_Strengths": [
        "1v1 ability, chance creation, wide attacking role",
        "Goal threat, inside movement, 1v1 ability, pace, transition threat",
        "Chance creation, passing, crosses, set pieces, advanced pressing",
        "Goal threat, movement into goal areas, 1v1 ability, defensive support",
        "Chance creation, movement, passing, pressing, positional flexibility"
    ],

    "Main_Risk": [
        "Lower goal threat + structure dependence",
        "Limited defensive contribution + creation secondary",
        "Lower goal threat + limited 1v1 ability",
        "Lower chance creation + below-baseline pressing",
        "Lower goal threat + limited 1v1 ability"
    ],

    "Unknown": [
        "Transferability of creative and 1v1 output to another attacking structure",
        "Whether goal threat can be maintained against settled defenses and in another structure",
        "Whether creative value can translate to a role requiring greater goal threat",
        "Whether goal threat can be maintained when transition space is limited",
        "How effectively his creation-oriented profile translates to another attacking structure"
    ],

    "Evidence_Needed": [
        "Match video across different tactical situations + tactical analysis of role",
        "Match video against settled defenses + tactical analysis outside transition situations",
        "Match video in different attacking roles + analysis of goal involvement and positioning",
        "Match video against deeper defenses + analysis of pressing and chance creation",
        "Match video in different attacking structures + analysis of goal threat and 1v1 situations"
    ]
}

candidate_uncertainty_summary=pd.DataFrame(candidate_uncertainty_summary)

final_candidate_summary = {

    "Candidate": [
        "Nusa",
        "El Mala",
        "Ibrahimovic",
        "Roca",
        "Moleiro"
    ],

    "Attacking_Profile": [
        "Creator-oriented LW",
        "Goal-Focused Attacker",
        "Creator",
        "Goal-Focused / Low Creation",
        "Creator / Low Goal Threat"
    ],

    "Performance_Fit": [
        "Strong 1v1 and chance-creation output, but below the high-performance xG threshold.",
        "Strong goal threat and 1v1 output, with high xG/90 and frequent movement into attacking spaces.",
        "Strong chance-creation output through passing, crosses and movement, but below the high-performance goal-threat reference.",
        "Strong goal threat and movement into scoring areas, while chance creation and pressing remain below baseline.",
        "Strong chance-creation output and positional contribution, below the high-performance goal-threat reference and the supporting 1v1 threshold."
    ],

    "Tactical_Fit": [
        "Wide-to-inside attacker who contributes through 1v1 actions, movement and chance creation within a high/wide role.",
        "Left-sided attacker who moves inside, attacks space and uses pace and 1v1 ability to threaten in transition.",
        "Central/wide creator who contributes through passing, crosses, movement and advanced pressing.",
        "Wide attacker who moves inside, attacks goal areas and provides defensive support and transition involvement.",
        "Left-sided creator who moves between wide and central areas and contributes through movement, passing and pressing."
    ],

    "Recruitment_Context": [
    "Age 21 | 2,048 Understat minutes | RB Leipzig | Contract 2029 | Market value €32M",
    "Age 19 | 1,965 Understat minutes | 1. FC Köln | Contract 2031 | Market value €45M",
    "Age 20 | 2,196 Understat minutes | FC Augsburg | Contract 2027 | Market value €10M",
    "Age 21 | 1,463 Understat minutes | Olympiacos | Contract 2029 | Market value €6M",
    "Age 22 | 2,535 Understat minutes | Villarreal | Contract 2030 | Market value €50M"
    ],

    "Main_Risk": [
        "Lower goal threat and dependence on his current tactical structure.",
        "Limited defensive contribution and creation is secondary to his goal-focused profile.",
        "Lower goal threat and limited reliance on individual 1v1 ability.",
        "Lower chance creation and below-baseline pressing.",
        "Lower goal threat and limited 1v1 output."
    ],

    "Key_Unknown": [
        "Whether his creative and 1v1 output transfers effectively to a different attacking structure.",
        "Whether he can maintain his goal threat against settled defenses and within a different tactical structure.",
        "Whether his creative value can translate to a role requiring greater goal threat.",
        "Whether he can maintain his goal threat when transition space is limited.",
        "How effectively his creation-oriented profile translates to another attacking structure."
    ],

    "Recruitment_Question": [
        "How transferable are Nusa's strengths outside Leipzig's current tactical structure?",
        "Can El Mala maintain his goal threat against settled defenses and within a different tactical structure?",
        "Can Ibrahimovic's creative value translate into a system requiring greater goal threat?",
        "Can Roca maintain his goal threat when there is less transition space?",
        "How effectively would Moleiro's creation-oriented profile translate into our club's attacking structure?"
    ],

    "Investigation_Status": [
        "Deep Investigation Complete",
        "Deep Investigation Complete",
        "Deep Investigation Complete",
        "Deep Investigation Complete",
        "Deep Investigation Complete"
    ]
}

final_candidate_summary=pd.DataFrame(final_candidate_summary)


# print(final_candidate_summary.to_string())

# ============================================================
# POWER BI EXPORT DATASET
# ============================================================
# One flat dataset for all Power BI pages:
# Performance + Methodology + Recruitment Context + Investigation

# Use the already enriched candidate dataset created above.
powerbi_recruitment_data = eligible_playtime_candidates.copy()

# Keep the candidate name consistent with the investigation summary.
# The summary uses "El Mala" while the analytical data may use the
# source player name.
investigation_name_map = {
    "Nusa": "Nusa",
    "El Mala": "El Mala",
    "Ibrahimovic": "Ibrahimovic",
    "Roca": "Roca",
    "Moleiro": "Moleiro",
}

powerbi_recruitment_data["Investigation_Candidate"] = (
    powerbi_recruitment_data["player_name"]
    .astype(str)
    .str.lower()
    .str.replace("_", " ", regex=False)
)

def match_investigation_candidate(player_name):
    name = str(player_name).lower()
    if "nusa" in name:
        return "Nusa"
    if "el mala" in name:
        return "El Mala"
    if "ibrahimovic" in name:
        return "Ibrahimovic"
    if "roca" in name:
        return "Roca"
    if "moleiro" in name:
        return "Moleiro"
    return None

powerbi_recruitment_data["Investigation_Candidate"] = (
    powerbi_recruitment_data["player_name"]
    .apply(match_investigation_candidate)
)

# Rename source fields into clean Power BI-friendly names.
powerbi_recruitment_data = powerbi_recruitment_data.rename(columns={
    "player_name": "Player",
    "league": "League",
    "understat_minutes": "Understat minutes",
    "fotmob_minutes": "FotMob minutes",
    "xG_per_90": "xG/90",
    "xA_per_90": "xA/90",
    "expected_contribution_per_90": "Expected contribution/90",
    "successful_dribbles_per_90": "Successful dribbles/90",
    "chances_created_per_90": "Chances created/90",
    "defensive_actions_per_90": "Defensive actions/90",
    "recoveries_per_90": "Recoveries/90",
    "possession_won_final_3rd_per_90": "Possession won final third/90",
    "profile": "Attacking Profile",
    "Meets_goal_threat_threshold": "Meets goal-threat threshold",
    "Meets_chance_creation_threshold": "Meets chance-creation threshold",
    "Meets_1v1_threshold": "Meets 1v1 threshold",
    "Meets_defensive_actions_baseline": "Meets defensive baseline",
    "Meets_recoveries_baseline": "Meets recovery baseline",
    "Meets_pressing_baseline": "Meets pressing baseline",
    "age_2026_07_01": "Age",
    "current_club": "Current club",
    "contract_expires": "Contract expiry",
    "contract_window": "Contract window",
    "market_value_in_eur": "Market value",
})

# Add the final investigation layer.
investigation_export = final_candidate_summary.rename(columns={
    "Candidate": "Investigation_Candidate",
    "Performance_Fit": "Performance Fit",
    "Tactical_Fit": "Tactical Fit",
    "Main_Risk": "Main Risk",
    "Key_Unknown": "Key Unknown",
    "Recruitment_Question": "Recruitment Question",
    "Investigation_Status": "Investigation Status",
})[
    [
        "Investigation_Candidate",
        "Performance Fit",
        "Tactical Fit",
        "Main Risk",
        "Key Unknown",
        "Recruitment Question",
        "Investigation Status",
    ]
]

powerbi_recruitment_data = powerbi_recruitment_data.merge(
    investigation_export,
    on="Investigation_Candidate",
    how="left"
)

# Final Power BI schema.
powerbi_columns = [
    # Performance
    "Player",
    "League",
    "Understat minutes",
    "FotMob minutes",
    "xG/90",
    "xA/90",
    "Expected contribution/90",
    "Successful dribbles/90",
    "Chances created/90",
    "Defensive actions/90",
    "Recoveries/90",
    "Possession won final third/90",

    # Methodology
    "Attacking Profile",
    "Meets goal-threat threshold",
    "Meets chance-creation threshold",
    "Meets 1v1 threshold",
    "Meets defensive baseline",
    "Meets recovery baseline",
    "Meets pressing baseline",

    # Recruitment context
    "Age",
    "Current club",
    "Contract expiry",
    "Contract window",
    "Market value",

    # Investigation
    "Performance Fit",
    "Tactical Fit",
    "Main Risk",
    "Key Unknown",
    "Recruitment Question",
    "Investigation Status",
]

# Keep only fields needed by Power BI.
powerbi_recruitment_data = powerbi_recruitment_data[
    [column for column in powerbi_columns if column in powerbi_recruitment_data.columns]
].copy()

# Clean date formatting for Power BI.
if "Contract expiry" in powerbi_recruitment_data.columns:
    powerbi_recruitment_data["Contract expiry"] = pd.to_datetime(
        powerbi_recruitment_data["Contract expiry"],
        errors="coerce"
    ).dt.date

# Export one clean flat CSV.
powerbi_export_path = Path(__file__).resolve().parent / "powerbi_recruitment_data.csv"

powerbi_recruitment_data.to_csv(
    powerbi_export_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nPower BI export created:")
print(powerbi_export_path)
print("\nPower BI columns:")
print(powerbi_recruitment_data.columns.tolist())
print("\nRows exported:", len(powerbi_recruitment_data))
