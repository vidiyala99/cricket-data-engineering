CREATE OR REPLACE VIEW impact_of_toss_home_games AS
WITH toss_analysis AS (
    SELECT
        id AS match_id,
        team1 AS home_team,
        toss_winner,
        winner,
        CASE 
            WHEN team1 = toss_winner THEN TRUE
            ELSE FALSE
        END AS home_team_won_toss,
        CASE 
            WHEN team1 = winner THEN TRUE
            ELSE FALSE
        END AS home_team_won_match
    FROM
        matches
    WHERE
        result != 'no result'
)
SELECT
    home_team_won_toss,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN home_team_won_match THEN 1 ELSE 0 END) AS matches_won,
    SUM(CASE WHEN NOT home_team_won_match THEN 1 ELSE 0 END) AS matches_lost,
    ROUND(100.0 * SUM(CASE WHEN home_team_won_match THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_percentage,
    ROUND(100.0 * SUM(CASE WHEN NOT home_team_won_match THEN 1 ELSE 0 END) / COUNT(*), 2) AS loss_percentage
FROM
    toss_analysis
GROUP BY
    home_team_won_toss
ORDER BY
    home_team_won_toss DESC;
