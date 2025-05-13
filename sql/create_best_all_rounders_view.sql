CREATE OR REPLACE VIEW best_all_rounders_season AS
WITH runs_per_season AS (
    SELECT
        season,
        batsman AS player,
        SUM(runs_batsman) AS total_runs
    FROM
        deliveries_updated
    GROUP BY
        season, batsman
),
wickets_per_season AS (
    SELECT
        season,
        bowler AS player,
        COUNT(*) AS total_wickets
    FROM
        deliveries_updated
    WHERE
        player_out IS NOT NULL
        AND wicket_type IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
    GROUP BY
        season, bowler
)
SELECT
    r.season,
    r.player,
    r.total_runs,
    w.total_wickets
FROM
    runs_per_season r
JOIN
    wickets_per_season w
ON
    r.season = w.season AND r.player = w.player
WHERE
    r.total_runs >= 300
    AND w.total_wickets >= 10
ORDER BY
    r.season ASC,
    r.total_runs DESC;
