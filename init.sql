CREATE TABLE IF NOT EXISTS raw_data (
    id          SERIAL PRIMARY KEY,
    payload     JSONB NOT NULL,
    fetched_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
 
CREATE INDEX IF NOT EXISTS idx_raw_data_payload ON raw_data USING GIN (payload);