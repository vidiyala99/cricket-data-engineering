CREATE OR REPLACE VIEW best_all_rounders_season AS
WITH runs_per_season AS (
    SELECT
        m.season,
        d.batsman AS player,
        SUM(d.batsman_runs) AS total_runs
    FROM
        deliveries d
    JOIN
        matches m ON d.match_id = m.id
    GROUP BY
        m.season, d.batsman
),
wickets_per_season AS (
    SELECT
        m.season,
        d.bowler AS player,
        COUNT(*) AS total_wickets
    FROM
        deliveries d
    JOIN
        matches m ON d.match_id = m.id
    WHERE
        d.player_dismissed IS NOT NULL
        AND d.dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
    GROUP BY
        m.season, d.bowler
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
