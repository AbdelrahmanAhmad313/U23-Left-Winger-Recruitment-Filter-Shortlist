create database FootballAnalytics

use FootballAnalytics

create table candidate_players(
player_key  int primary key,
player_name nvarchar(100) not null,
league varchar(50) not null,
club_2025_26 nvarchar(50) not null,
date_of_birth date not null,
age_2026_07_01 int not null,
position nvarchar(50) not null,
foot nvarchar(10) not null,
contract_expires date ,
current_club nvarchar(50) not null,
)



create table source_identity(
player_key int primary key,
transfermarkt_id nvarchar(25),
understat_id nvarchar(25),
fotmob_id nvarchar(25),
CONSTRAINT FK_source_identity_candidate_players
    FOREIGN KEY (player_key)
    REFERENCES candidate_players(player_key)
)


create table understat_stats(
player_key int primary key,
understat_games int,
understat_minutes int,
understat_goals int,
understat_xG decimal(10,2),
understat_assists int,
understat_xA decimal(10,2),
understat_shots int,
understat_key_passes int,
understat_npxG decimal(10,2),
CONSTRAINT FK_understat_stats_candidate_players
    FOREIGN KEY (player_key)
    REFERENCES candidate_players(player_key)
)

create table fotmob_stats(
player_key int primary key,
fotmob_goals int,
fotmob_assists int,
goals_and_assists int,
fotmob_rating decimal(10,2),
fotmob_minutes int,
goals_per_90 decimal(10,2),
fotmob_xG decimal(10,2),
xG_per_90 decimal(10,2),
xGOT decimal(10,2),
shots_on_target_per_90 decimal(10,2),
shots_per_90 decimal(10,2),
accurate_passes_per_90 decimal(10,2),
big_chances_created int,
chances_created int,
accurate_long_balls_per_90 decimal(10,2),
fotmob_xA decimal(10,2),
xA_per_90 decimal(10,2),
xG_and_xA_per_90 decimal(10,2),
successful_dribbles_per_90 decimal(10,2),
big_chances_missed int,
defensive_actions_per_90 decimal(10,2),
recoveries_per_90 decimal(10,2),
possession_won_final_3rd_per_90 decimal(10,2),
CONSTRAINT FK_fotmob_stats_candidate_players
    FOREIGN KEY (player_key)
    REFERENCES candidate_players(player_key)
)

create table market_value(
player_key int primary key,
valuation_date date,
market_value_in_eur int,
CONSTRAINT FK_market_value_candidate_players
    FOREIGN KEY (player_key)
    REFERENCES candidate_players(player_key)
)


create table candidate_data_status(
player_key int primary key,
data_group nvarchar(50),
data_status nvarchar(50),
CONSTRAINT FK_candidate_data_status_candidate_players
    FOREIGN KEY (player_key)
    REFERENCES candidate_players(player_key)
)


-- Every candidate in our U23 LW pool, along with their Understat xG

select c.player_key, c.player_name,c.league,c.current_club,c.club_2025_26,u.understat_minutes, u.understat_xG
from candidate_players c left join 
understat_stats u
on c.player_key = u.player_key   
order by u.understat_xG desc

-- Among candidates with at least 900 Understat minutes, which players produced the most xG per 90 minutes?

select c.player_key , c.player_name , (u.understat_xG/u.understat_minutes) * 90 as understat_xG_per_90
from candidate_players c inner join
understat_stats u 
on c.player_key = u.player_key
where u.understat_minutes>=900
order by understat_xG_per_90 desc

--Okay, xG is useful, but I don't want a shortlist based purely on scoring.
--I want to see which candidates combine attacking output with chance creation.


select c.player_key , c.player_name ,c.league,u.understat_minutes,u.understat_xG,u.understat_xA, u.understat_xG+u.understat_xA as total_expected_contribution
from candidate_players c inner join
understat_stats u 
on c.player_key = u.player_key
where u.understat_minutes>=900
order by total_expected_contribution desc

--Give me the candidates who have both Understat and FotMob data, so we can compare information across the two sources.

select c.player_key,c.player_name,c.league,u.understat_xG,u.understat_xA,f.fotmob_xG,f.fotmob_xA
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
inner join fotmob_stats f
on c.player_key = f.player_key

--How many candidates have Understat data, FotMob data, both, or neither?

SELECT data_group, COUNT(*) AS candidate_count
FROM candidate_data_status
GROUP BY data_group;


--How many candidates have sufficient performance data for analysis, and how many don't?

SELECT data_status, COUNT(*) AS candidate_count
FROM candidate_data_status
GROUP BY data_status;

--Show me every candidate who has a known market value,
--along with their current club and valuation date, ordered from highest to lowest market value

select c.player_name,c.current_club,m.valuation_date,m.market_value_in_eur
from candidate_players c
inner join market_value m
on c.player_key = m.player_key
order by m.market_value_in_eur desc

--Among players with at least 900 Understat minutes, show me their market value alongside their xG and xA.

select c.player_name,c.league,u.understat_minutes, u.understat_xG,u.understat_xA ,m.market_value_in_eur
from candidate_players c
inner join understat_stats  u
on c.player_key = u.player_key
inner join market_value m
on m.player_key = c.player_key
where u.understat_minutes >=900
ORDER BY m.market_value_in_eur DESC

--Among players with at least 900 Understat minutes, 
--which players generate the most expected attacking contribution relative to their market value?

select c.player_name,c.league,u.understat_minutes, u.understat_xG,u.understat_xA,
u.understat_xG+u.understat_xA as total_expected_contribution ,m.market_value_in_eur,
(u.understat_xG+u.understat_xA) /nullif(m.market_value_in_eur/1000000.0,0) as expected_contribution_per_million
from candidate_players c
inner join understat_stats  u
on c.player_key = u.player_key
inner join market_value m
on m.player_key = c.player_key
where u.understat_minutes >=900
ORDER BY expected_contribution_per_million  DESC

--Which candidates have contracts expiring within the next 24 months from our reference date of 1 July 2026?

select player_name, league,current_club,contract_expires
from candidate_players
where contract_expires between '2026-07-01' and '2028-07-01'
order by contract_expires

--Show me the candidates who are 21 or younger on our reference date.

select player_name,league,date_of_birth ,age_2026_07_01
from candidate_players
where age_2026_07_01 <= 21
ORDER BY age_2026_07_01 ASC;

--For candidates with both sources available, 
--show me their Understat and FotMob minutes so we can identify any significant discrepancy between the sources.

select c.player_name , c.league , u.understat_minutes,f.fotmob_minutes ,ABS(u.understat_minutes - f.fotmob_minutes) as minutes_difference
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
inner join fotmob_stats f
on f.player_key = c.player_key
order by minutes_difference desc

--Show me every candidate who has no performance data from either Understat or FotMob.

select c.player_name , c.league , c.current_club,cd.data_group,cd.data_status
from candidate_players c
inner join candidate_data_status cd
on c.player_key=cd.player_key
where cd.data_group = 'Neither'

--Among candidates with at least 900 Understat minutes, show their expected attacking contribution per 90 minutes.

select c.player_name,c.league,u.understat_minutes,u.understat_xG,u.understat_xA,
((u.understat_xG+u.understat_xA)/u.understat_minutes)*90 as expected_contribution_per_90
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
where u.understat_minutes>=900
order by expected_contribution_per_90 desc

--Among candidates with at least 900 Understat minutes, show me their xG/90, xA/90, and total expected contribution/90

select c.player_name,c.league,u.understat_minutes,u.understat_xG,u.understat_xA,
(u.understat_xG/u.understat_minutes)*90 as xG_per_90,
(u.understat_xA/u.understat_minutes)*90 as xA_per_90,
((u.understat_xG+u.understat_xA)/u.understat_minutes)*90 as expected_contribution_per_90
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
where u.understat_minutes>=900
order by expected_contribution_per_90 desc

--Classify candidates according to their expected attacking contribution per 90.

WITH player_stats AS (
    SELECT 
        c.player_name,
        c.league,
        ((u.understat_xG + u.understat_xA) * 90.0) 
            / NULLIF(u.understat_minutes, 0) AS expected_contribution_per_90
    FROM candidate_players c
    INNER JOIN understat_stats u
        ON c.player_key = u.player_key
    WHERE u.understat_minutes >= 900
)
SELECT
    player_name,
    league,
    expected_contribution_per_90,
    CASE 
        WHEN expected_contribution_per_90 >= 0.7 THEN 'High'
        WHEN expected_contribution_per_90 >= 0.4 THEN 'Medium'
        ELSE 'Low'
    END AS attacking_profile
FROM player_stats
ORDER BY expected_contribution_per_90 DESC

--Among candidates with enough Understat minutes, 
--show me their attacking output and their FotMob dribbling/chance-creation metrics when those are available.

select c.player_name,c.league,u.understat_minutes,u.understat_xG ,u.understat_xA,f.successful_dribbles_per_90,f.chances_created
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
left join fotmob_stats f
on c.player_key = f.player_key
where u.understat_minutes>=900
order by f.successful_dribbles_per_90 desc


--Among players with at least 900 Understat minutes,
--which candidates have a known market valuation,
--and what is their expected attacking contribution relative to their valuation?

select c.player_name,c.league,u.understat_minutes, u.understat_xG,u.understat_xA,
u.understat_xG+u.understat_xA as total_expected_contribution ,m.market_value_in_eur,
(u.understat_xG+u.understat_xA) /nullif(m.market_value_in_eur/1000000.0,0) as expected_contribution_per_million
from candidate_players c
inner join understat_stats  u
on c.player_key = u.player_key
inner join market_value m
on m.player_key = c.player_key
where u.understat_minutes >=900
ORDER BY expected_contribution_per_million  DESC

--Show me the U23 candidates with at least 900 minutes whose contracts expire within the next 24 months,
--along with their attacking output.

select c.player_name, c.league,c.current_club,c.contract_expires ,
u.understat_minutes, u.understat_xG,u.understat_xA , ((u.understat_xG+u.understat_xA)/ u.understat_minutes)*90 as expected_contribution_per_90
from candidate_players c
inner join understat_stats u 
on c.player_key = u.player_key
where (u.understat_minutes>=900 ) and
(c.contract_expires between '2026-07-01' and '2028-07-01')
order by contract_expires


--Which candidates have no performance data from either Understat or FotMob?

select c.player_name , c.league , c.current_club,cd.data_group,cd.data_status
from candidate_players c
inner join candidate_data_status cd
on c.player_key=cd.player_key
where cd.data_group = 'Neither'

--Which leagues have at least 3 candidates with ≥900 Understat minutes?

SELECT 
    c.league,
    COUNT(*) AS candidate_players
FROM candidate_players c
INNER JOIN understat_stats u
    ON c.player_key = u.player_key
WHERE u.understat_minutes >= 900
GROUP BY c.league
HAVING  count(*) >= 3


--Find candidates whose expected contribution per 90 is above the average expected contribution per 90 
--among all candidates with ≥900 Understat minutes.

WITH player_stats AS (
    SELECT 
        c.player_name,
        c.league,
        ((u.understat_xG + u.understat_xA) * 90.0) 
            / NULLIF(u.understat_minutes, 0) AS expected_contribution_per_90
    FROM candidate_players c
    INNER JOIN understat_stats u
        ON c.player_key = u.player_key
    WHERE u.understat_minutes >= 900
)
select player_name,league,expected_contribution_per_90
from player_stats 
where expected_contribution_per_90 > (
    SELECT AVG(expected_contribution_per_90)
    FROM player_stats
)
order by expected_contribution_per_90 desc


----

select c.player_name,c.league,c.current_club,c.contract_expires,
u.understat_minutes,(u.understat_xG/nullif(u.understat_minutes,0))*90.0 as xG_per_90,
(u.understat_xA/nullif(u.understat_minutes,0))*90.0 as xA_per_90,
(u.understat_xG/nullif(u.understat_minutes,0))*90.0 +(u.understat_xA/nullif(u.understat_minutes,0))*90.0 as expected_contribution_per_90,
f.successful_dribbles_per_90,
f.chances_created,
m.market_value_in_eur
from candidate_players c
inner join understat_stats u
on c.player_key = u.player_key
left join fotmob_stats f
on c.player_key = f.player_key
inner join market_value m
on c.player_key =m.player_key
where u.understat_minutes>=900