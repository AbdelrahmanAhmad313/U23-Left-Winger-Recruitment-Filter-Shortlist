import pandas as pd
from src.matching.matching_player import result_matched_players

df = pd.DataFrame(result_matched_players)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nMinutes:")
print(df["minutes"].describe())

numeric_columns = [
    "games",
    "minutes",
    "goals",
    "xG",
    "assists",
    "xA",
    "shots",
    "key_passes",
    "npxG"
]

df[numeric_columns] = df[numeric_columns].apply(
    pd.to_numeric,
    errors="coerce"
)

# print("\nData types after conversion:")
# print(df.dtypes)

# print("\nMissing values after conversion:")
# print(df.isnull().sum())

# print("\nMinutes:")
# print(df["minutes"].describe())

performance_pool = df[df["minutes"] >= 900].copy()

print("Players meeting 900-minute threshold:", len(performance_pool))
print("\nPlayers:")
print(
    performance_pool[
        ["player_name", "league", "transfermarkt_club", "minutes"]
    ].sort_values("minutes", ascending=False).to_string(index=False)
)

performance_pool["goals_per90"] = (
    performance_pool["goals"] / performance_pool["minutes"] * 90
)

performance_pool["xG_per90"] = (
    performance_pool["xG"] / performance_pool["minutes"] * 90
)

performance_pool["assists_per90"] = (
    performance_pool["assists"] / performance_pool["minutes"] * 90
)

performance_pool["xA_per90"] = (
    performance_pool["xA"] / performance_pool["minutes"] * 90
)

print(
    performance_pool[
        [
            "player_name",
            "league",
            "minutes",
            "goals_per90",
            "xG_per90",
            "assists_per90",
            "xA_per90"
        ]
    ].sort_values("goals_per90", ascending=False).to_string(index=False)
)