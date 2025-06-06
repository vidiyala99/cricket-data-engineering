DROP VIEW IF EXISTS top_powerplay_bowlers;

CREATE VIEW top_powerplay_bowlers AS
WITH valid_pp_balls AS (
    SELECT 
        bowler,
        CASE WHEN wide_runs = 0 AND noball_runs = 0 THEN 1 ELSE 0 END AS legal_ball,
        total_runs,
        CASE WHEN player_dismissed IS NOT NULL 
             AND dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
             THEN 1 ELSE 0
        END AS is_wicket
    FROM 
        deliveries_updated
    WHERE 
        over BETWEEN 1 AND 6
),
bowler_stats AS (
    SELECT
        bowler,
        SUM(legal_ball) AS balls_bowled,
        SUM(total_runs) AS runs_conceded,
        SUM(is_wicket) AS wickets_taken
    FROM 
        valid_pp_balls
    GROUP BY 
        bowler
),
filtered AS (
    SELECT * 
    FROM bowler_stats 
    WHERE wickets_taken >= 10
)
SELECT
    bowler,
    balls_bowled,
    runs_conceded,
    wickets_taken,
    ROUND(runs_conceded / NULLIF(balls_bowled / 6.0, 0), 2) AS economy_rate
FROM 
    filtered
ORDER BY 
    economy_rate ASC, 
    wickets_taken DESC;
