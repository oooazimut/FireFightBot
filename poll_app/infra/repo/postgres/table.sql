create table if not exists sprinkler (
    id SERIAL PRIMARY KEY,
    tank_level DOUBLE PRECISION DEFAULT 0,
    pressure DOUBLE PRECISION DEFAULT 0,
    crit_pressure BOOLEAN DEFAULT FALSE,
    pump_is_running BOOLEAN DEFAULT FALSE,
    sensor_fault BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_spr_timestamp ON sprinkler (timestamp);
