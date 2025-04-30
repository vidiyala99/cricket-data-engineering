DROP VIEW IF EXISTS top_death_batters;
CREATE OR REPLACE VIEW top_death_batters AS
WITH death_stats AS (
    SELECT
        m.season,
        d.batsman,
        COUNT(*) FILTER (WHERE d.wide_runs = 0) AS balls_faced,
        SUM(d.batsman_runs) AS runs_scored
    FROM deliveries d
    JOIN matches m ON d.match_id = m.id
    WHERE d.over BETWEEN 16 AND 20
    GROUP BY m.season, d.batsman
),
season_filtered AS (
    SELECT * FROM death_stats WHERE runs_scored >= 250
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

    UNION

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
ORDER BY season ASC, strike_rate DESC;
