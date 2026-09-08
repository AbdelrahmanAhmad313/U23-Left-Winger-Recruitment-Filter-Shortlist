import json
from pathlib import Path

from understatapi import UnderstatClient


output_path = Path("../Project 1 — U23 Left-Winger Recruitment Filter & Shortlist/data/raw/understat/bundesliga_2025_26.json")

with UnderstatClient() as understat:
    data = understat.league(
        "Bundesliga"
    ).get_player_data(
        "2025"
    )

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved {len(data)} player records to:")
print(output_path)