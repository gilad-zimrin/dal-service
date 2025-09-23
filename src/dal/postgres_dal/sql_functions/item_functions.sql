# TODO create my own sql functions
CREATE OR REPLACE FUNCTION app.item_create(payload jsonb)
RETURNS items AS $$
DECLARE
    r items%ROWTYPE;
BEGIN
    INSERT INTO app.items (name, description)
    VALUES (payload->>'name', (payload->>'description')::text)
    RETURNING * INTO r;
    RETURN r;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION app.item_update(id_param bigint, payload jsonb)
RETURNS items AS $$
DECLARE
    r items%ROWTYPE;
BEGIN
    UPDATE app.items
    SET
      name = COALESCE(payload->>'name', name),
      description = COALESCE(payload->>'description', description)
    WHERE id = id_param
    RETURNING * INTO r;
    RETURN r;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION app.item_delete(id_param bigint)
RETURNS boolean AS $$
BEGIN
    DELETE FROM app.items WHERE id = id_param;
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
