CREATE OR REPLACE FUNCTION demo.customer_create(customer_payload jsonb)
RETURNS demo.customers AS $$
DECLARE
    inserted_customer demo.customers%ROWTYPE;
BEGIN
    INSERT INTO demo.customers (username, password, email, name, age, location)
    VALUES (
        customer_payload->>'username',
        customer_payload->>'password',
        customer_payload->>'email',
        customer_payload->>'name',
        (customer_payload->>'age')::INT,
        customer_payload->>'location'
    )
    RETURNING * INTO inserted_customer;

    RETURN inserted_customer;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION demo.customer_update(
    target_customer_id BIGINT,
    customer_payload   jsonb
)
RETURNS demo.customers AS $$
DECLARE
    updated_customer demo.customers%ROWTYPE;
BEGIN
    UPDATE demo.customers
    SET
        username = COALESCE(customer_payload->>'username', username),
        password = COALESCE(customer_payload->>'password', password),
        email    = COALESCE(customer_payload->>'email', email),
        name     = COALESCE(customer_payload->>'name', name),
        age      = COALESCE((customer_payload->>'age')::INT, age),
        location = COALESCE(customer_payload->>'location', location)
    WHERE customer_id = target_customer_id
    RETURNING * INTO updated_customer;

    RETURN updated_customer;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION demo.customer_delete(target_customer_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    deleted_count INT;
BEGIN
    DELETE FROM demo.customers WHERE customer_id = target_customer_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count > 0;
END;
$$ LANGUAGE plpgsql;
