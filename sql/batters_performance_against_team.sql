SELECT 
    batsman,
    bowling_team AS opponent_team,
    SUM(batsman_runs) AS total_runs,
    COUNT(batsman) AS total_balls_faced,
    ROUND(SUM(batsman_runs) / NULLIF(COUNT(batsman), 0), 2) AS strike_rate,
    COUNT(CASE WHEN player_dismissed = batsman THEN 1 END) AS dismissals
FROM 
    deliveries_updated
GROUP BY 
    batsman, bowling_team
ORDER BY 
    batsman, bowling_team;
