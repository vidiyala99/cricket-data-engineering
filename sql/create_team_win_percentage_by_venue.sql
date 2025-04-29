CREATE OR REPLACE VIEW team_win_percentage_by_venue AS
SELECT
    team,
    venue,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) AS matches_won,
    ROUND(100.0 * SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_percentage
FROM (
    SELECT id, team1 AS team, venue, winner
    FROM matches
    WHERE result != 'no result'

    UNION ALL

    SELECT id, team2 AS team, venue, winner
    FROM matches
    WHERE result != 'no result'
) combined
GROUP BY team, venue
ORDER BY team, win_percentage DESC;
