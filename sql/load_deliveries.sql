-- load_deliveries.sql
CREATE TEMP TABLE temp_deliveries (
    match_id INTEGER,
    inning TEXT,
    batting_team TEXT,
    batsman TEXT,
    non_striker TEXT,
    bowler TEXT,
    runs_batsman INTEGER,
    runs_extras INTEGER,
    runs_total INTEGER,
    extras_type TEXT,
    wicket_type TEXT,
    player_out TEXT
);

COPY temp_deliveries (
    match_id, inning, batting_team, batsman, non_striker, 
    bowler, runs_batsman, runs_extras, runs_total, 
    extras_type, wicket_type, player_out
)
FROM STDIN WITH CSV HEADER DELIMITER ',';

-- Upsert (Insert or Update Only if NULL)
INSERT INTO deliveries (match_id, inning, batting_team, batsman, non_striker, 
                        bowler, runs_batsman, runs_extras, runs_total, 
                        extras_type, wicket_type, player_out)
SELECT * FROM temp_deliveries
ON CONFLICT (match_id, inning, batsman, bowler) 
DO UPDATE SET 
    runs_batsman = COALESCE(deliveries.runs_batsman, EXCLUDED.runs_batsman),
    runs_extras = COALESCE(deliveries.runs_extras, EXCLUDED.runs_extras),
    runs_total = COALESCE(deliveries.runs_total, EXCLUDED.runs_total),
    extras_type = COALESCE(deliveries.extras_type, EXCLUDED.extras_type),
    wicket_type = COALESCE(deliveries.wicket_type, EXCLUDED.wicket_type),
    player_out = COALESCE(deliveries.player_out, EXCLUDED.player_out);
