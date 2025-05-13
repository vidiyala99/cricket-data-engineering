DROP VIEW IF EXISTS top_powerplay_batters;

CREATE VIEW top_powerplay_batters AS
WITH powerplay_stats AS (
    SELECT
        season,
        batsman,
        COUNT(*) - COUNT(CASE WHEN wide_runs > 0 THEN 1 END) AS balls_faced,  -- Excluding wide deliveries
        SUM(batsman_runs) AS runs_scored
    FROM 
        deliveries_updated
    WHERE 
        over BETWEEN 1 AND 6
    GROUP BY 
        season, batsman
)
SELECT
    season,
    batsman,
    balls_faced,
    runs_scored,
    ROUND(runs_scored * 100.0 / NULLIF(balls_faced, 0), 2) AS strike_rate
FROM 
    powerplay_stats
WHERE 
    runs_scored >= 300
ORDER BY 
    season ASC, 
    strike_rate DESC, 
    runs_scored DESC;
