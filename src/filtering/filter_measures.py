import requests
import json

fotmob_metrics = { # name : url_name
"Goals" : "goals" ,
"Assists" : "goal_assist" ,
"Goals and Assists" : "_goals_and_goal_assist" ,
"FotMob rating" : "rating" ,
"Minutes played" : "mins_played" ,
"Goals per 90" : "goals_per_90" ,
"xG" : "expected_goals" ,
"xG per 90" : "expected_goals_per_90" ,
"xGOT" : "expected_goalsontarget" ,
"Shots on target per 90 ": "ontarget_scoring_att" ,
"Shots per 90" : "total_scoring_att" ,
"Accurate passes per 90 ": "accurate_pass" ,
"Big chances created" : "big_chance_created" ,
"Chances created" : "total_att_assist" ,
"Accurate long balls per 90 ": "accurate_long_balls" ,
"xA" : "expected_assists" ,
"xA per 90" : "expected_assists_per_90" ,
"xG and xA per 90" : "_expected_goals_and_expected_assists_per_90" ,
"Successful dribbles per 90" : "won_contest" ,
"Big chances missed ": "big_chance_missed" ,
"Defensive actions per 90" : "defensive_contributions" ,
"Recoveries per 90" : "ball_recovery" ,
"Possession won final 3rd per 90" : "poss_won_att_3rd" ,
}

league_id = 54
season_id = 26891 
# laliga 2025-26 season id = 27233


for name,json_name in fotmob_metrics.items():
    
    url = f"https://data.fotmob.com/stats/{league_id}/season/{season_id}/{json_name}.json"
    response = requests.get(url)
    
    print("Status code:", response.status_code)
    if response.status_code == 200:
        with open(
        f"data/raw/fotmob/bundesliga_2025_26/{name}.json",
        "w",
        encoding="utf-8"
        ) as file:
            json.dump(response.json(), file)

        print("Saved successfully")

    else:
        print("Request failed:", response.status_code)
    


# data = response.json()

# print(type(data))

# print(data.keys() if isinstance(data, dict) else "Not a dictionary")

# print(data)

