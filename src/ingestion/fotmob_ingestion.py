import requests
import json

url = "https://www.fotmob.com/api/data/leagues"
bundesliga_id=54
laliga_id= 87

params = {
    "id": laliga_id,
    "season": "2025/2026"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()

print("Top-level keys:")
print(data.keys())

# print("\nAvailable seasons:")
# print(data["allAvailableSeasons"])
# # print(data["table"])

# print("\nSeason objects:")
# print(data["seasons"])
print("\nLaLiga details:")
print(data["details"])

print("\nNumber of stat categories:")
print(len(data["stats"]["players"]))
print(data["stats"]["players"][0])

print("\nStat categories:")
for stat in data["stats"]["players"]:
    print(
        stat["header"],
        ":",
        stat["participant"]["stat"]["name"],
        ",",
        # stat["fetchAllUrl"],
    )
    

