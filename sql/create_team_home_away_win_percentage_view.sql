CREATE OR REPLACE VIEW team_home_away_win_percentage AS
WITH home_matches AS (
    SELECT
        team1 AS team,
        'home' AS location,
        COUNT(*) AS total_matches,
        SUM(CASE WHEN team1 = winner THEN 1 ELSE 0 END) AS matches_won
    FROM matches
    WHERE result != 'no result'
    GROUP BY team1
),
away_matches AS (
    SELECT
        team2 AS team,
        'away' AS location,
        COUNT(*) AS total_matches,
        SUM(CASE WHEN team2 = winner THEN 1 ELSE 0 END) AS matches_won
    FROM matches
    WHERE result != 'no result'
    GROUP BY team2
),
combined AS (
    SELECT * FROM home_matches
    UNION ALL
    SELECT * FROM away_matches
)
SELECT
    team,
    location,
    total_matches,
    matches_won,
    ROUND(100.0 * matches_won / total_matches, 2) AS win_percentage
FROM combined
ORDER BY team, location;
