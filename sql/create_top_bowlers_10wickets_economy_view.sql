CREATE OR REPLACE VIEW top_bowlers_10wickets_economy AS
WITH bowler_stats AS (
    SELECT
        season,
        bowler,
        COUNT(*) FILTER (WHERE player_dismissed IS NOT NULL 
                         AND dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')) AS total_wickets,
        SUM(total_runs) AS total_runs_conceded,
        COUNT(CASE WHEN wide_runs = 0 AND noball_runs = 0 THEN 1 END) AS valid_balls
    FROM
        deliveries_updated
    GROUP BY
        season, bowler
)
SELECT
    season,
    bowler,
    total_wickets,
    ROUND(total_runs_conceded / (valid_balls / 6.0), 2) AS economy_rate
FROM
    bowler_stats
WHERE
    total_wickets >= 10
    AND (total_runs_conceded / (valid_balls / 6.0)) <= 9.0
ORDER BY
    season ASC,
    total_wickets DESC;
