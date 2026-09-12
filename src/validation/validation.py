import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cleaning.cleaning import all_candidates_fotmob


def check_duplicate_players(df):
    duplicate_players = df[
        df.duplicated(
            subset=["league", "player_name"],
            keep=False
        )
    ]

    return len(duplicate_players)


def check_negative_values(df, columns):
    violations = 0

    for column in columns:
        violations += (
            df[column].notna()
            & (df[column] < 0)
        ).sum()

    return violations


def check_goals_vs_shots(df):
    violations = df[
        df["understat_goals"].notna()
        & df["understat_shots"].notna()
        & (
            df["understat_goals"]
            > df["understat_shots"]
        )
    ]

    return len(violations)

def determine_status(row):

    if row["violations"] == 0:
        return "PASS"

    return row["severity"]


def run_validation(df):

    understat_value_columns = [
        "understat_games",
        "understat_minutes",
        "understat_goals",
        "understat_xG",
        "understat_assists",
        "understat_xA",
        "understat_shots",
        "understat_key_passes",
        "understat_npxG"
    ]

    results = []

    results.append({
    "category": "Structural Integrity",
    "check": "Duplicate player records",
    "violations": check_duplicate_players(df),
    "severity": "FAIL"
})

    results.append({
        "category": "Data Quality",
        "check": "Negative Understat values",
        "violations": check_negative_values(
            df,
            understat_value_columns
        ),
    "severity": "FAIL"
    })

    results.append({
        "category": "Logical Consistency",
        "check": "Goals greater than shots",
        "violations": check_goals_vs_shots(df),
    "severity": "FAIL"
    })
    results.append({
    "category": "Source Coverage",
    "check": "Missing Understat data",
    "violations": df["understat_id"].isna().sum(),
    "severity": "WARNING"
})
    results.append({
        "category": "Logical Consistency",
        "check": "Goals with zero shots",
        "violations": len(
            df[
                df["understat_goals"].notna()
                & df["understat_shots"].notna()
                & (df["understat_goals"] > 0)
                & (df["understat_shots"] == 0)
            ]
        ),
        "severity": "FAIL"
    })

    results.append({
        "category": "Logical Consistency",
        "check": "Positive xG with zero shots",
        "violations": len(
            df[
                df["understat_xG"].notna()
                & df["understat_shots"].notna()
                & (df["understat_xG"] > 0)
                & (df["understat_shots"] == 0)
            ]
        ),
        "severity": "FAIL"
    })

    results.append({
        "category": "Logical Consistency",
        "check": "npxG greater than xG",
        "violations": len(
            df[
                df["understat_npxG"].notna()
                & df["understat_xG"].notna()
                & (
                    df["understat_npxG"]
                    > df["understat_xG"]
                )
            ]
        ),
        "severity": "FAIL"
    })
    
    performance_columns = [
        "understat_goals",
        "understat_xG",
        "understat_assists",
        "understat_xA",
        "understat_shots",
        "understat_key_passes"
    ]

    results.append({
        "category": "Logical Consistency",
        "check": "Zero minutes with positive performance",
        "violations": len(
            df[
                df["understat_minutes"].notna()
                & (df["understat_minutes"] == 0)
                & (
                    df[performance_columns]
                    .fillna(0)
                    .sum(axis=1) > 0
                )
            ]
        ),
        "severity": "FAIL"
    })
    
    fotmob_numeric_columns = [
        "fotmob_goals",
        "fotmob_assists",
        "goals_and_assists",
        "fotmob_rating",
        "fotmob_minutes",
        "goals_per_90",
        "fotmob_xG",
        "xG_per_90",
        "xGOT",
        "shots_on_target_per_90",
        "shots_per_90",
        "accurate_passes_per_90",
        "big_chances_created",
        "chances_created",
        "accurate_long_balls_per_90",
        "fotmob_xA",
        "xA_per_90",
        "xG_and_xA_per_90",
        "successful_dribbles_per_90",
        "big_chances_missed",
        "defensive_actions_per_90",
        "recoveries_per_90",
        "possession_won_final_3rd_per_90"
    ]

    results.append({
        "category": "Data Quality",
        "check": "Negative FotMob values",
        "violations": check_negative_values(
            df,
            fotmob_numeric_columns
        ),
        "severity": "FAIL"
    })
    
    results.append({
        "category": "Logical Consistency",
        "check": "Goals + assists consistency",
        "violations": len(
            df[
                df["fotmob_goals"].notna()
                & df["fotmob_assists"].notna()
                & df["goals_and_assists"].notna()
                & (
                    (
                        df["fotmob_goals"]
                        + df["fotmob_assists"]
                    )
                    != df["goals_and_assists"]
                )
            ]
        ),
        "severity": "FAIL"
    })
    
    fotmob_per90_columns = [
        "goals_per_90",
        "xG_per_90",
        "shots_on_target_per_90",
        "shots_per_90",
        "accurate_passes_per_90",
        "accurate_long_balls_per_90",
        "xA_per_90",
        "xG_and_xA_per_90",
        "successful_dribbles_per_90",
        "defensive_actions_per_90",
        "recoveries_per_90",
        "possession_won_final_3rd_per_90"
    ]

    per90_violations = 0

    for column in fotmob_per90_columns:
        per90_violations += len(
            df[
                df["fotmob_minutes"].notna()
                & (df["fotmob_minutes"] == 0)
                & df[column].notna()
                & (df[column] > 0)
            ]
        )

    results.append({
        "category": "Logical Consistency",
        "check": "Per-90 values with zero minutes",
        "violations": per90_violations,
        "severity": "FAIL"
    })    
    
    # ---------------------------------------------------------
    # FotMob per-90 mathematical consistency
    # ---------------------------------------------------------

    per90_checks = [
        (
            "Goals per 90 consistency",
            "fotmob_goals",
            "goals_per_90"
        ),
        (
            "xG per 90 consistency",
            "fotmob_xG",
            "xG_per_90"
        ),
        (
            "xA per 90 consistency",
            "fotmob_xA",
            "xA_per_90"
        )
    ]

    for check_name, total_column, per90_column in per90_checks:

        mask = (
            df[total_column].notna()
            & df["fotmob_minutes"].notna()
            & df[per90_column].notna()
            & (df["fotmob_minutes"] > 0)
        )

        calculated_per90 = (
            df.loc[mask, total_column]
            / df.loc[mask, "fotmob_minutes"]
            * 90
        )

        difference = (
            calculated_per90
            - df.loc[mask, per90_column]
        )

        violations = (difference.abs() > 0.02).sum()

        results.append({
            "category": "Logical Consistency",
            "check": check_name,
            "violations": violations,
            "severity": "FAIL"
        })
        
    # ---------------------------------------------------------
    # Cross-source minutes consistency
    # ---------------------------------------------------------

    minutes_mask = (
        df["understat_minutes"].notna()
        & df["fotmob_minutes"].notna()
    )

    minutes_difference = (
        df.loc[minutes_mask, "understat_minutes"]
        - df.loc[minutes_mask, "fotmob_minutes"]
    ).abs()

    results.append({
        "category": "Source Consistency",
        "check": "Large cross-source minutes difference",
        "violations": (minutes_difference > 90).sum(),
        "severity": "WARNING"
    })
    
    # ---------------------------------------------------------
    # Duplicate source IDs
    # ---------------------------------------------------------

    for column in [
        "transfermarkt_code",
        "understat_id",
        "fotmob_id"
    ]:

        duplicate_ids = df[
            df[column].notna()
            & df.duplicated(
                subset=[column],
                keep=False
            )
        ]

        results.append({
            "category": "Structural Integrity",
            "check": f"Duplicate {column}",
            "violations": len(duplicate_ids),
            "severity": "FAIL"
        })
        
    # ---------------------------------------------------------
    # Required candidate fields
    # ---------------------------------------------------------

    required_columns = [
        "player_name",
        "league",
        "transfermarkt_club",
        "transfermarkt_code"
    ]

    missing_required_values = df[required_columns].isna().sum().sum()

    results.append({
        "category": "Structural Integrity",
        "check": "Missing required candidate fields",
        "violations": missing_required_values,
        "severity": "FAIL"
    })
    
    results.append({
        "category": "Structural Integrity",
        "check": "Candidate universe size",
        "violations": abs(len(df) - 50),
        "severity": "FAIL"
    })
    
    
    validation_report = pd.DataFrame(results)

    validation_report["status"] = validation_report.apply(
    determine_status,
    axis=1
)

    print("\n" + "=" * 60)
    print("DATA VALIDATION REPORT")
    print("=" * 60)

    print(
        validation_report.to_string(index=False)
    )

    print("\n" + "=" * 60)

    if (validation_report["status"] == "FAIL").any():
        print("FINAL RESULT: FAIL")
    elif (validation_report["status"] == "WARNING").any():
        print("FINAL RESULT: PASS WITH WARNINGS")
    else:
        print("FINAL RESULT: PASS")

    print("=" * 60)


if __name__ == "__main__":
    run_validation(all_candidates_fotmob)