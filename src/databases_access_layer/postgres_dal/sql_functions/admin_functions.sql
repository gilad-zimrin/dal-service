CREATE OR REPLACE FUNCTION demo.admin_create(admin_payload jsonb)
RETURNS demo.admins AS $$
DECLARE
    inserted_admin demo.admins%ROWTYPE;
BEGIN
    INSERT INTO demo.admins (username, password, email)
    VALUES (
        admin_payload->>'username',
        admin_payload->>'password',
        admin_payload->>'email'
    )
    RETURNING * INTO inserted_admin;

    RETURN inserted_admin;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION demo.admin_update(
    target_admin_id BIGINT,
    admin_payload   jsonb
)
RETURNS demo.admins AS $$
DECLARE
    updated_admin demo.admins%ROWTYPE;
BEGIN
    UPDATE demo.admins
    SET
        username = COALESCE(admin_payload->>'username', username),
        password = COALESCE(admin_payload->>'password', password),
        email    = COALESCE(admin_payload->>'email', email)
    WHERE admin_id = target_admin_id
    RETURNING * INTO updated_admin;

    RETURN updated_admin;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION demo.admin_delete(target_admin_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    deleted_count INT;
BEGIN
    DELETE FROM demo.admins WHERE admin_id = target_admin_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count > 0;
END;
$$ LANGUAGE plpgsql;
