CREATE SCHEMA IF NOT EXISTS demo;


CREATE TABLE IF NOT EXISTS demo.items (
    item_id      BIGSERIAL PRIMARY KEY,
    name         TEXT NOT NULL,
    description  TEXT,
    price        NUMERIC(12,2) NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT now()
);
