CREATE OR REPLACE VIEW top_batters_350runs_130sr AS
WITH batsman_stats AS (
    SELECT
        season,
        batsman,
        SUM(batsman_runs) AS total_runs,
        COUNT(*) - COUNT(CASE WHEN wide_runs > 0 THEN 1 END) AS balls_faced -- Excluding wides from balls faced
    FROM
        deliveries_updated
    GROUP BY
        season, batsman
)
SELECT
    season,
    batsman,
    total_runs,
    balls_faced,
    ROUND((total_runs * 100.0) / NULLIF(balls_faced, 0), 2) AS strike_rate
FROM
    batsman_stats
WHERE
    total_runs >= 350
    AND (total_runs * 100.0) / NULLIF(balls_faced, 0) >= 130
ORDER BY
    season ASC,
    total_runs DESC;
