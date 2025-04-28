CREATE OR REPLACE VIEW top_bowlers_10wickets_economy AS
WITH bowler_stats AS (
    SELECT
        m.season,
        d.bowler,
        COUNT(*) FILTER (WHERE d.player_dismissed IS NOT NULL 
                         AND d.dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')) AS total_wickets,
        SUM(d.total_runs) AS total_runs_conceded,
        COUNT(CASE WHEN d.wide_runs = 0 AND d.noball_runs = 0 THEN 1 END) AS valid_balls
    FROM
        deliveries d
    JOIN
        matches m ON d.match_id = m.id
    GROUP BY
        m.season, d.bowler
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
