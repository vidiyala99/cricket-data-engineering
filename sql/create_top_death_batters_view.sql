DROP VIEW IF EXISTS top_death_batters;
CREATE OR REPLACE VIEW top_death_batters AS
WITH death_stats AS (
    SELECT
        season,
        batsman,
        COUNT(*) - COUNT(CASE WHEN wide_runs > 0 THEN 1 END) AS balls_faced,
        SUM(batsman_runs) AS runs_scored
    FROM 
        deliveries_updated
    WHERE 
        over BETWEEN 16 AND 20
    GROUP BY 
        season, batsman
),
season_filtered AS (
    SELECT * 
    FROM death_stats 
    WHERE runs_scored >= 250
),
overall_totals AS (
    SELECT
        batsman,
        SUM(runs_scored) AS total_runs,
        SUM(balls_faced) AS total_balls
    FROM death_stats
    GROUP BY batsman
    HAVING SUM(runs_scored) >= 500
),
combined AS (
    SELECT
        CAST(season AS TEXT) AS season,
        batsman,
        balls_faced,
        runs_scored
    FROM season_filtered

    UNION ALL

    SELECT
        'All-Time' AS season,
        batsman,
        total_balls AS balls_faced,
        total_runs AS runs_scored
    FROM overall_totals
)
SELECT
    season,
    batsman,
    balls_faced,
    runs_scored,
    ROUND(runs_scored * 100.0 / NULLIF(balls_faced, 0), 2) AS strike_rate
FROM combined
ORDER BY 
    season ASC, strike_rate DESC;
