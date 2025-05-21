WITH batsman_stats AS (
    SELECT
        d.batsman,
        d.batting_team AS team,
        COUNT(*) FILTER (WHERE d.wide_runs = 0) AS balls_faced,
        SUM(d.batsman_runs) AS total_runs,
        COUNT(*) FILTER (WHERE d.player_dismissed = d.batsman) AS dismissals
    FROM deliveries_updated d
    GROUP BY d.batsman, d.batting_team
),
basra_calc AS (
    SELECT
        batsman,
        team,
        total_runs,
        balls_faced,
        dismissals,
        CASE 
            WHEN dismissals = 0 THEN total_runs 
            ELSE ROUND(CAST(total_runs AS NUMERIC) / dismissals, 2) 
        END AS average,
        CASE 
            WHEN balls_faced = 0 THEN 0 
            ELSE ROUND((CAST(total_runs AS NUMERIC) / balls_faced) * 100, 2) 
        END AS strike_rate
    FROM batsman_stats
),
final_leaderboard AS (
    SELECT *,
        ROUND(average + strike_rate, 2) AS basra
    FROM basra_calc
    WHERE total_runs >= 250
)
SELECT * FROM final_leaderboard
ORDER BY basra DESC
LIMIT 50;
