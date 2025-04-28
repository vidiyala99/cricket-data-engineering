CREATE OR REPLACE VIEW top_batters_350runs_130sr AS
WITH batsman_stats AS (
    SELECT
        m.season,
        d.batsman,
        SUM(d.batsman_runs) AS total_runs,
        COUNT(CASE WHEN d.wide_runs = 0 THEN 1 END) AS balls_faced
    FROM
        deliveries d
    JOIN
        matches m ON d.match_id = m.id
    GROUP BY
        m.season, d.batsman
)
SELECT
    season,
    batsman,
    total_runs,
    balls_faced,
    ROUND((total_runs * 100.0) / balls_faced, 2) AS strike_rate
FROM
    batsman_stats
WHERE
    total_runs >= 350
    AND (total_runs * 100.0) / balls_faced >= 130
ORDER BY
    season ASC,
    total_runs DESC;
