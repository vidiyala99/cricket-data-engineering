WITH batter_runs AS (
    SELECT 
        season,
        batsman,
        SUM(runs_batsman) AS total_runs,
        COUNT(*) AS balls_faced,
        ROUND(SUM(runs_batsman) * 100.0 / NULLIF(COUNT(*), 0), 2) AS strike_rate
    FROM 
        deliveries_updated
    GROUP BY season, batsman
),

top_5_batters AS (
    SELECT 
        season,
        batsman,
        total_runs,
        strike_rate,
        RANK() OVER (PARTITION BY season ORDER BY total_runs DESC) AS rank
    FROM 
        batter_runs
)

SELECT 
    season,
    batsman,
    total_runs,
    strike_rate
FROM 
    top_5_batters 
WHERE 
    rank <= 5
ORDER BY 
    season ASC, total_runs DESC;
