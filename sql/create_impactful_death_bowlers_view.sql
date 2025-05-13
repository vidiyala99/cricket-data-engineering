CREATE OR REPLACE VIEW impactful_death_bowlers AS
WITH player_appearance AS (
    SELECT 
        match_id, 
        batsman, 
        MIN(over * 6 + ball) AS first_appearance
    FROM 
        deliveries_updated
    GROUP BY match_id, batsman
),
top_order_batsmen AS (
    SELECT 
        match_id, 
        batsman
    FROM (
        SELECT 
            match_id, 
            batsman, 
            ROW_NUMBER() OVER (PARTITION BY match_id ORDER BY first_appearance ASC) AS batting_position
        FROM player_appearance
    ) ranked
    WHERE batting_position <= 6
),
death_wickets AS (
    SELECT 
        CAST(bowler AS VARCHAR(200)) AS bowler,  -- Explicitly matching table data type
        COUNT(*) AS top_order_wickets_in_death
    FROM 
        deliveries_updated d
    JOIN 
        top_order_batsmen t 
        ON d.match_id = t.match_id AND d.player_dismissed = t.batsman
    WHERE 
        d.over BETWEEN 16 AND 20
        AND d.player_dismissed IS NOT NULL
        AND d.dismissal_kind IN ('bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket')
    GROUP BY 
        bowler
)
SELECT 
    bowler, 
    top_order_wickets_in_death
FROM 
    death_wickets
ORDER BY 
    top_order_wickets_in_death DESC;
