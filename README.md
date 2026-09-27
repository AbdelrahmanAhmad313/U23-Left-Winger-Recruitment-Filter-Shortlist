# U23 Left-Winger Recruitment Filter & Shortlist

A football recruitment analytics project focused on identifying and investigating U23 left-wingers who could realistically develop into a replacement for an existing starting left winger within the next 12–24 months.

The project combines football performance data, recruitment context, statistical analysis, qualitative investigation, and Power BI visualization to simulate a professional recruitment workflow.

---

## Recruitment Problem

A hypothetical mid-table European club has a 30-year-old starting left winger whose contract expires in approximately 18 months and whose performance is beginning to decline.

The Head of Recruitment asks:

> **"Find us a shortlist of U23 left wingers across accessible European leagues who could realistically develop into his replacement within the next 12–24 months."**

The objective is therefore not simply to find the players with the highest statistics.

The analysis considers:

- Goal threat
- Chance creation
- 1v1 ability
- Defensive contribution
- Pressing contribution
- Off-ball movement
- Playing time
- Age
- Contract situation
- Financial context
- Tactical role
- League context
- Recruitment risks and unknowns

The final output is a **shortlist for deeper recruitment investigation**, not a definitive signing recommendation.

---

## Project Workflow

The project follows a structured recruitment analytics workflow:

1. Project Brief
2. Data Acquisition
3. Data Understanding
4. Data Cleaning & Validation
5. Data Modeling
6. SQL Analysis
7. Python Analysis
8. Recruitment Methodology
9. Candidate Investigation
10. Power BI Dashboard
11. Recruitment Report
12. GitHub Documentation
13. LinkedIn Presentation
14. Final Recruiter Review

---

## Data Sources

The project combined data from:

- **Understat** — xG, xA and playing-time data
- **FotMob** — supplementary 2025/26 performance statistics
- **Transfermarkt** — age, position, club, contract and market-value context
- **Historical Transfermarkt market-value data** — supplementary valuation history

Raw and processed datasets are not included in this public repository.

---

## Player Population

The initial recruitment universe contained **50 U23 left-winger candidates**.

The player pool was progressively narrowed using playing-time and data-quality requirements.

### Recruitment Funnel

**50 U23 candidates**  
→ **9 players with ≥900 Understat minutes**  
→ **5 candidates selected for deeper investigation**

The final five were selected using the attacking profile framework and supporting performance indicators, followed by qualitative recruitment-context investigation.

### Analytical Population

The final analytical population contained **9 players** who met the minimum requirement of 900 Understat minutes.

The population consisted of players from:

- Bundesliga
- LaLiga

The analysis intentionally kept the population small and focused rather than expanding it with players who lacked sufficient playing-time evidence.

---

## Analytical Approach

The project separates the recruitment process into several layers.

### 1. Attacking Profile

The primary attacking dimensions were:

- xG/90 — goal threat
- xA/90 — chance creation

These metrics were used to classify players into different attacking profiles.

Profiles included:

- All-Round Attacker
- Goal-Focused Attacker
- Goal-Focused / Low Creation
- Creator
- Creator / Low Goal Threat
- Balanced Attacker
- Lower Attacking Output

The purpose of the framework was to understand **what type of attacker each player represents**, rather than simply ranking players by a single number.

---

### 2. Supporting Performance Indicators

Additional metrics were used to understand the wider player profile:

- Successful dribbles/90
- Defensive actions/90
- Recoveries/90
- Possession won in the final third/90

These indicators were treated as supporting evidence rather than being combined into a single overall score.

---

### 3. Recruitment Context

Performance data was combined with contextual information including:

- Age
- Current club
- Playing time
- Contract expiry
- Market-value estimate
- League

Market value was treated as **financial context**, not as an expected transfer fee.

Contract expiry was treated as recruitment context rather than evidence that a player is automatically available.

---

## Recruitment Methodology

The recruitment methodology translated the original scouting requirements into measurable evidence.

| Requirement            | Metric / Evidence             | Priority                | Threshold              |
| ---------------------- | ----------------------------- | ----------------------- | ---------------------- |
| Goal threat            | xG/90                         | High performance        | ≥75th percentile       |
| Chance creation        | xA/90                         | High performance        | ≥75th percentile       |
| 1v1 ability            | Successful dribbles/90        | Supporting preference   | ≥45th percentile       |
| Defensive contribution | Defensive actions/90          | Baseline                | ≥35th percentile       |
| Defensive contribution | Recoveries/90                 | Baseline                | ≥35th percentile       |
| Pressing contribution  | Possession won final third/90 | Baseline                | ≥40th percentile       |
| Off-ball movement      | Scouting/video                | Important — qualitative | Qualitative            |
| Age                    | Age on 2026-07-01             | Eligibility             | U23                    |
| Playing time           | Understat/FotMob minutes      | Evidence requirement    | ≥900 Understat minutes |
| Contract               | Contract expiry               | Contextual              | No hard threshold      |
| Financial context      | Market-value estimate         | Contextual              | No hard threshold      |

### Why No Composite Score?

A single composite recruitment score was intentionally avoided.

Different players can contribute in different ways.

For example:

- One player may provide greater goal threat.
- Another may provide stronger chance creation.
- Another may offer better 1v1 ability.
- Another may provide greater defensive involvement.

Rather than forcing these different player types into one ranking, the analysis first identifies their profiles and then investigates whether those profiles fit the recruitment problem.

---

## Candidate Selection

The final deep-investigation group contained five players:

- **Antonio Nusa**
- **Said El Mala**
- **Arijon Ibrahimovic**
- **Joel Roca**
- **Alberto Moleiro**

These players were selected for deeper investigation based on their attacking profiles and supporting indicators.

The selection process did not use an arbitrary points system or composite score.

Instead, the process considered:

1. Primary attacking profile
2. Supporting performance indicators
3. Player archetype
4. Recruitment context
5. Potential risks
6. Questions requiring further scouting investigation

The five candidates therefore represent **different potential player profiles**, rather than five players ranked from first to fifth.

---

# Candidate Investigation

## Antonio Nusa

### Profile

**Creator-oriented Left Winger**

### Performance Fit

Nusa's profile is driven by:

- Chance creation
- 1v1 ability
- Defensive involvement
- Recoveries

His goal threat is below the high-performance threshold used in the methodology.

### Tactical Fit

Nusa operates in a wide attacking role and can move into inside areas while remaining involved in chance creation and 1v1 situations.

His role also includes defensive responsibilities and pressing from wide areas.

### Recruitment Context

- Age: 21
- Understat minutes: 2,048
- Club: RB Leipzig
- Contract: 2029
- Market-value estimate: €32M

### Main Risk

Lower goal threat and potential dependence on his current tactical structure.

### Key Unknown

How transferable are Nusa's creative and 1v1 strengths outside Leipzig's current tactical structure?

### Evidence Required

- Match video across different tactical situations
- Defensive responsibilities after possession loss
- Pressing behavior
- Off-ball movement
- Performance in different tactical structures

---

## Said El Mala

### Profile

**Goal-Focused Attacker**

### Performance Fit

El Mala's profile is driven by:

- High goal threat
- 1v1 ability
- Runs into attacking space
- Transition threat

Chance creation is secondary to his goal-focused profile.

### Tactical Fit

El Mala starts from the left and frequently moves toward central areas before attacking the goal.

His pace, ball control and ability to attack space support a direct attacking role.

### Recruitment Context

- Age: 19
- Understat minutes: 1,965
- Club: 1. FC Köln
- Contract: 2031
- Market-value estimate: €45M

### Main Risk

Limited defensive contribution and lower chance-creation output.

### Key Unknown

Can El Mala maintain his goal threat against settled defenses and within a different tactical structure?

### Evidence Required

- Match video against deeper defensive blocks
- Performance outside transition situations
- Defensive behavior
- Tactical role in different structures

---

## Arijon Ibrahimovic

### Profile

**Creator**

### Performance Fit

Ibrahimovic's profile is driven by:

- Chance creation
- Passing
- Crosses
- Movement to receive
- Set-piece contribution

His goal threat is below the high-performance threshold and his 1v1 output is not a primary strength.

### Tactical Fit

He can operate in central and wider attacking areas.

His creative contribution comes more from passing, positioning, crosses and movement than from repeatedly attacking defenders 1v1.

He also provides advanced pressing involvement.

### Recruitment Context

- Age: 20
- Understat minutes: 2,196
- Club: FC Augsburg
- Contract: 2027
- Market-value estimate: €10M

### Main Risk

Lower goal threat and limited reliance on 1v1 ability.

### Key Unknown

Can Ibrahimovic's creative value translate into a system that requires greater goal threat from the left-wing position?

### Evidence Required

- Video across different attacking roles
- Positioning analysis
- Goal-involvement analysis
- Assessment of his role in a more goal-focused attacking structure

---

## Joel Roca

### Profile

**Goal-Focused / Low Creation**

### Performance Fit

Roca's profile is driven by:

- Goal threat
- Movement into goal areas
- 1v1 ability
- Defensive support

Chance creation is secondary.

### Tactical Fit

Roca operates from wide areas and can move inside toward goal.

His movement and positioning contribute to his attacking output, while he can also track back and support the fullback.

### Recruitment Context

- Age: 21
- Understat minutes: 1,463
- Club: Olympiacos
- Contract: 2029
- Market-value estimate: €6M

### Main Risk

Lower chance creation and below-baseline final-third pressing contribution.

### Key Unknown

Can Roca maintain his goal threat when there is less transition space available?

### Evidence Required

- Match video against deeper defensive blocks
- Chance-creation analysis
- Pressing behavior
- Performance outside transition situations

---

## Alberto Moleiro

### Profile

**Creator / Low Goal Threat**

### Performance Fit

Moleiro's profile is driven by:

- Chance creation
- Movement
- Passing
- Defensive contribution
- Pressing
- Positional flexibility

His goal threat and 1v1 output are below the high/supporting thresholds.

### Tactical Fit

Moleiro can operate from wide and more central areas.

He frequently moves inside, combines with teammates and contributes through positioning, passing and movement rather than relying primarily on direct 1v1 actions.

He also contributes to pressing and defensive recovery.

### Recruitment Context

- Age: 22
- Understat minutes: 2,535
- Club: Villarreal CF
- Contract: 2030
- Market-value estimate: €50M

### Main Risk

Lower goal threat and limited reliance on 1v1 ability.

### Key Unknown

How effectively would Moleiro's creation-oriented profile translate into our club's attacking structure?

### Evidence Required

- Video in different tactical structures
- Goal-threat assessment
- 1v1 analysis
- Evaluation of his role when less space is available

---

# Recruitment Context

Recruitment performance cannot be evaluated separately from context.

The project therefore considered:

### Playing Time

Playing time was used as an evidence requirement.

All final analytical candidates had at least 900 Understat minutes.

### Market Value

Transfermarkt market value was used as a financial context indicator.

It does **not** represent:

- An expected transfer fee
- A guaranteed selling price
- A player's true market price

### Contract Situation

Contract expiry was used to identify potential recruitment timing considerations.

However, contract expiry alone does not establish:

- Availability
- Transfer willingness
- Actual contract terms
- Negotiation difficulty

### League Context

The analytical population included players from Bundesliga and LaLiga.

League differences were not normalized because the final analytical population was small.

Instead, league context is treated as a limitation and an additional consideration for recruitment.

---

# SQL Analysis

SQL was used to query the structured football database and investigate:

- Player populations
- Performance metrics
- Player comparisons
- Performance analysis
- Recruitment-context analysis
- Candidate analysis
- Supporting metric investigation

The SQL workflow helped validate the underlying data and support the recruitment analysis before moving into Python and Power BI.

---

# Python Analysis

Python was used for:

- Data ingestion
- Data cleaning
- Player matching
- Data validation
- Transformation
- Feature engineering
- Statistical analysis
- Percentile calculations
- Recruitment methodology
- Candidate investigation
- Visualization

The Python workflow was structured into reusable modules covering ingestion, cleaning, matching, modeling, analysis and visualization.

---

# Power BI Dashboard

The Power BI dashboard contains three pages.

## Page 1 — Recruitment Overview

Answers:

> **How do the identified U23 LW candidates differ in attacking profile and supporting performance indicators?**

Includes:

- Analytical population KPI
- Deep-investigation player KPI
- League count
- Attacking profile count
- Candidate population table
- xG/90 vs xA/90 attacking profile scatter
- Dynamic supporting-performance chart

---

## Page 2 — Candidate Comparison

Answers:

> **How does an individual candidate's performance profile compare with the analytical population?**

Includes:

- Candidate selector
- Player context
- Current club
- League
- Age
- Market-value estimate
- Playing time
- Contract
- Attacking profile
- Core performance metrics
- Recruitment criteria status
- Six-metric percentile comparison

The percentile analysis compares each selected player's performance against the nine-player analytical population.

---

## Page 3 — Recruitment Investigation

Answers:

> **What does the current evidence suggest about the candidate's recruitment fit, and what still requires investigation?**

Includes:

- Tactical Fit
- Performance Fit
- Known Strengths
- Main Risk
- Recruitment Question
- Key Unknown
- Evidence Needed
- Investigation Status

The page is designed to connect quantitative analysis with qualitative recruitment reasoning.

---

# Recruitment Report

The project also includes a professional recruitment report covering:

1. Executive Summary
2. Recruitment Brief
3. Data Sources and Methodology
4. Analytical Population
5. Performance Analysis
6. Recruitment Methodology
7. Candidate Shortlist
8. Deep Candidate Investigations
9. Recruitment Context
10. Risks and Unknowns
11. Methodology Limitations
12. Final Recruitment Interpretation

The report is intended to simulate a professional recruitment-analysis deliverable rather than a purely technical data-science report.

---

# Limitations

This analysis has several important limitations.

### Small Analytical Population

The final analytical population contains only nine players with at least 900 Understat minutes.

Therefore, percentile thresholds are decision rules within this population and should not be interpreted as estimates of the wider U23 winger population.

### League Context

The population combines Bundesliga and LaLiga players without league normalization.

Differences in:

- Tactical style
- Team strength
- Possession
- Match tempo
- League environment

may influence player statistics.

### Attacking Profile

xG/90 and xA/90 provide useful information about attacking output but do not explain how that output is generated.

They do not directly capture:

- Tactical role
- Shot selection
- Movement quality
- Decision-making
- Positioning
- Teammate influence

### Pressing

Possession won in the final third was used as a partial proxy for pressing contribution.

It does not directly measure:

- Pressing quality
- Pressing timing
- Pressing triggers
- Pressing lanes
- Team coordination
- Individual defensive decision-making

### Off-Ball Movement

Off-ball movement could not be reliably measured using the available dataset.

Video and scouting analysis are required to evaluate:

- Timing of runs
- Runs behind the defensive line
- Space creation
- Positioning
- Movement relative to teammates

### Market Value

Transfermarkt market value is an estimate and should not be interpreted as an expected transfer fee.

### Contract Situation

Contract expiry provides recruitment context but does not establish actual availability or transfer feasibility.

### Player Selection

No composite score was used.

The methodology prioritizes attacking profile first and uses supporting metrics and recruitment context to determine which players deserve deeper investigation.

### Recruitment Decision

The five selected players are **candidates for deeper recruitment investigation**, not definitive signing recommendations.

A final recruitment decision would require additional evidence including:

- Detailed video scouting
- Tactical fit analysis
- Injury history
- Character and mentality assessment
- Physical profiling
- Salary expectations
- Transfer-fee expectations
- Agent and contract information
- Club willingness to sell
- Adaptation risk
- Further league and team-context analysis

---

# Project Outputs

The repository contains the main public project outputs:

### Power BI Dashboard

`powerbi/U23 Left-Winger Recruitment Dashboard.pbix`

### Dashboard Screenshots

`powerbi/Screenshots/`

### Recruitment Report

`report/U23_Left_Winger_Recruitment_Report.pdf`

### SQL Analysis

`sql/FootballAnalytics.sql`

### Python Analysis

`src/`

Raw and processed datasets are intentionally excluded from the public repository.

---

# Technologies

- Python
- pandas
- requests
- understatapi
- matplotlib
- SQL
- Power BI
- Git
- GitHub

---

# Project Focus

This project demonstrates how football data can support a recruitment workflow by combining:

**Data acquisition → Data validation → Statistical analysis → Recruitment methodology → Candidate investigation → Contextual research → Dashboarding → Recruitment reporting**

The main objective was not to produce a ranking of players.

It was to demonstrate a structured process for turning football data into **recruitment-relevant evidence**, while clearly identifying what the data can answer and what still requires scouting and human judgment.

---

## Author

**Abdelrahman Ahmed Abdellatif**

Computer Science Student | Football Data & Recruitment Analytics

GitHub:  
https://github.com/AbdelrahmanAhmad313
