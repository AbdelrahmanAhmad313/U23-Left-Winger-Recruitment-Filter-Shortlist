import json
from pathlib import Path

file_path = Path("../Temp/Data/Raw/understat/bundesliga_2025_26.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Data type:", type(data))
print("Number of players:", len(data))
print("Fields:")
print(data[0].keys())

print("\nFirst player:")
print(data[0])