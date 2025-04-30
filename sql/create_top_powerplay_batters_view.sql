DROP VIEW IF EXISTS top_powerplay_batters;

CREATE VIEW top_powerplay_batters AS
WITH powerplay_stats AS (
    SELECT
        m.season,
        d.batsman,
        COUNT(*) FILTER (WHERE d.wide_runs = 0) AS balls_faced,
        SUM(d.batsman_runs) AS runs_scored
    FROM deliveries d
    JOIN matches m ON d.match_id = m.id
    WHERE d.over BETWEEN 1 AND 6
    GROUP BY m.season, d.batsman
)
SELECT
    season,
    batsman,
    balls_faced,
    runs_scored,
    ROUND(runs_scored * 100.0 / NULLIF(balls_faced, 0), 2) AS strike_rate
FROM powerplay_stats
WHERE runs_scored >= 300
ORDER BY season ASC, strike_rate DESC, runs_scored DESC;
