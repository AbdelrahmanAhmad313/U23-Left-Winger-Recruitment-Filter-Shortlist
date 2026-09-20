import matplotlib.pyplot as plt
import sys
from pathlib import Path
import pandas as pd 

sys.path.append(str(Path(__file__).resolve().parents[1]))
from analysis.analysis import eligible_playtime_candidates

# Visualize relationship between goal threat and chance creation

def goalAndChanceRelation(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Scatter by league
    for league, group in df.groupby("league"):
        ax.scatter(
            group["xG_per_90"],
            group["xA_per_90"],
            label=league,
            s=70,
            alpha=0.8
        )

    # Population average — xG/90
    ax.axvline(
        df["xG_per_90"].mean(),
        color="dimgray",
        linestyle="--",
        linewidth=2,
        label="Population Average — xG/90"
    )

    # Population average — xA/90
    ax.axhline(
        df["xA_per_90"].mean(),
        color="dimgray",
        linestyle=":",
        linewidth=2,
        label="Population Average — xA/90"
    )

    # Main title
    ax.set_title(
        "U23 Left-Winger Candidate Analysis",
        fontsize=14,
        fontweight="bold"
    )

    # Subtitle
    fig.suptitle(
        "xG/90 vs xA/90 — Bundesliga & LaLiga | 2025/26 | ≥900 Understat minutes",
        fontsize=11,
        y=0.94
    )

    # Axis labels
    ax.set_xlabel(
        "xG per 90",
        fontsize=12
    )

    ax.set_ylabel(
        "xA per 90",
        fontsize=12
    )

    # Extra room for Said El Mala
    x_min = df["xG_per_90"].min()
    x_max = df["xG_per_90"].max()

    ax.set_xlim(
        x_min,
        x_max + 0.04
    )

    # Custom annotation offsets
    annotation_offsets = {
        "Arijon Ibrahimovic": (0.02, -0.02),
        "Antonio Nusa": (0.015, 0.005),
        "Alberto Moleiro": (-0.035, -0.02)
    }

    # Player annotations
    for _, row in df.iterrows():

        player_name = row["player_name"]

        dx, dy = annotation_offsets.get(
            player_name,
            (0.005, 0.005)
        )

        ax.annotate(
            player_name,
            (
                row["xG_per_90"] + dx,
                row["xA_per_90"] + dy
            ),
            fontsize=9
        )

    # Legend
    ax.legend()

    fig.tight_layout(rect=[0, 0, 1, 0.91])

    return fig

# Visualize relationship between dribbling and chance creation

def dribblingAndChanceCreationRelation(df):
    fig , ax = plt.subplots(figsize=(12,6))
     
    for league, group in df.groupby("league"):
            ax.scatter(
             group["successful_dribbles_per_90"],
             group["chances_created_per_90"],
             label=league,
             s=70,
             alpha=0.8
             )
             
    # Average XG
    ax.axvline(
            df["successful_dribbles_per_90"].mean(),
            color="red",
            linestyle="--",
            linewidth=2,
            label="Avg successful dribbles per 90"
        )
    
        # Average XA
    ax.axhline(
            df["chances_created_per_90"].mean(),
            color="blue",
            linestyle="--",
            linewidth=2,
            label="Avg chances created per 90"
        )
    
    ax.set_xlabel("successful dribbles per 90", fontsize=12)
    ax.set_ylabel("chances created per 90", fontsize=12)
    title=f"successful dribbles per 90 and chances created per 90 Relation \n Corr= {(df["chances_created_per_90"].corr(df["successful_dribbles_per_90"])).round(2)}"
    
    ax.set_title(
            title,
            fontsize=12,
            fontweight="bold"
        )
    
    for _, row in df.iterrows():
            ax.annotate(
                row["player_name"],
                (row["successful_dribbles_per_90"], row["chances_created_per_90"]),
                fontsize=9
            )
    
    ax.legend()
    fig.tight_layout()

fig = goalAndChanceRelation(eligible_playtime_candidates)
plt.show()