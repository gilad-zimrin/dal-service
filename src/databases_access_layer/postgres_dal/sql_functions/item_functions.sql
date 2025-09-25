-- TODO document functions response types, create returns id, update returns full object, delete returns bool

CREATE OR REPLACE FUNCTION demo.item_create(item_payload jsonb)
RETURNS BIGINT AS $$
DECLARE
    new_item_id BIGINT;
BEGIN
    INSERT INTO demo.items (name, description, price)
    VALUES (
        item_payload->>'name',
        item_payload->>'description',
        (item_payload->>'price')::NUMERIC
    )
    RETURNING item_id INTO new_item_id;

    RETURN new_item_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION demo.item_update(
    target_item_id BIGINT,
    item_payload   jsonb
)
RETURNS demo.items AS $$
DECLARE
    updated_item demo.items%ROWTYPE;
BEGIN
    UPDATE demo.items
    SET
        name        = COALESCE(item_payload->>'name', name),
        description = COALESCE(item_payload->>'description', description),
        price       = COALESCE((item_payload->>'price')::NUMERIC, price)
    WHERE item_id = target_item_id
    RETURNING * INTO updated_item;

    RETURN updated_item;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION demo.item_delete(target_item_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    deleted_count INT;
BEGIN
    DELETE FROM demo.items WHERE item_id = target_item_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count > 0;
END;
$$ LANGUAGE plpgsql;
