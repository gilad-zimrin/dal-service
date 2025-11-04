CREATE SCHEMA IF NOT EXISTS demo;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'industry_enum') THEN
        CREATE TYPE demo.industry_enum AS ENUM (
            'Technology',
            'Finance',
            'Healthcare',
            'Retail',
            'Manufacturing'
        );
    END IF;
END$$;


CREATE TABLE IF NOT EXISTS demo.companies (
    company_id    BIGSERIAL PRIMARY KEY,
    name          TEXT UNIQUE NOT NULL,
    username      TEXT NOT NULL,
	password      TEXT NOT NULL,
    email         TEXT NOT NULL,
    location      TEXT,
    industry      demo.industry_enum NOT NULL,
    employees     INT,
    register_time TIMESTAMP without time zone DEFAULT now()
);


CREATE TABLE IF NOT EXISTS demo.customers (
    customer_id BIGSERIAL PRIMARY KEY,
    username    TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    email       TEXT NOT NULL,
    name        TEXT,
    age         INT,
    location    TEXT
);


CREATE TABLE IF NOT EXISTS demo.items (
    item_id     BIGSERIAL PRIMARY KEY,
    company_id  BIGINT NOT NULL REFERENCES demo.companies(company_id),
    name        TEXT NOT NULL,
    description TEXT,
    price       NUMERIC(12,2) NOT NULL,
    stock       INT NOT NULL DEFAULT 0,
    created_at  TIMESTAMP without time zone DEFAULT now()
);


CREATE TABLE IF NOT EXISTS demo.orders (
    order_id     BIGSERIAL PRIMARY KEY,
    customer_id  BIGINT NOT NULL REFERENCES demo.customers(customer_id),
    order_time   TIMESTAMP without time zone DEFAULT now()
);


CREATE TABLE IF NOT EXISTS demo.order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id      BIGINT NOT NULL REFERENCES demo.orders(order_id),
    item_id       BIGINT NOT NULL REFERENCES demo.items(item_id),
    quantity      INT NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(12,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS demo.admins (
    admin_id      BIGSERIAL PRIMARY KEY,
    username      TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email         TEXT,
    created_at    TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

