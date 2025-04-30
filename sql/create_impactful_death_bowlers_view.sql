CREATE OR REPLACE VIEW impactful_death_bowlers AS
SELECT
    bowler,
    COUNT(*) AS top_order_wickets_in_death
FROM deliveries
WHERE
    over BETWEEN 16 AND 20
    AND player_dismissed IS NOT NULL
    AND dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
    AND player_dismissed IN (
        SELECT DISTINCT batsman
        FROM (
            SELECT match_id, batsman, MIN(over * 6 + ball) AS first_appearance
            FROM deliveries
            GROUP BY match_id, batsman
            ORDER BY match_id, first_appearance
        ) ranked
        WHERE (
            SELECT COUNT(*)
            FROM (
                SELECT match_id, batsman, MIN(over * 6 + ball) AS fa
                FROM deliveries
                GROUP BY match_id, batsman
            ) r2
            WHERE r2.match_id = ranked.match_id
            AND r2.fa <= ranked.first_appearance
        ) <= 6  -- Top 6
    )
GROUP BY bowler
ORDER BY top_order_wickets_in_death DESC;
