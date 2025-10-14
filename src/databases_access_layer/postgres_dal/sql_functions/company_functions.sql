CREATE OR REPLACE FUNCTION demo.company_create(company_payload jsonb)
RETURNS demo.companies AS $$
DECLARE
    inserted_company demo.companies%ROWTYPE;
BEGIN
    INSERT INTO demo.companies (name, username, password, email, location, industry, employees, register_time)
    VALUES (
        company_payload->>'name',
        company_payload->>'username',
        company_payload->>'password',
        company_payload->>'email',
        company_payload->>'location',
        (company_payload->>'industry')::demo.industry_enum,
        (company_payload->>'employees')::INT,
        COALESCE((company_payload->>'register_time')::TIMESTAMPTZ, now())
    )
    RETURNING * INTO inserted_company;

    RETURN inserted_company;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION demo.company_update(
    target_company_id BIGINT,
    company_payload   jsonb
)
RETURNS demo.companies AS $$
DECLARE
    updated_company demo.companies%ROWTYPE;
BEGIN
    UPDATE demo.companies
    SET
        name      = COALESCE(company_payload->>'name', name),
        username  = COALESCE(company_payload->>'username', username),
        password  = COALESCE(company_payload->>'password', password),
        email     = COALESCE(company_payload->>'email', email),
        location  = COALESCE(company_payload->>'location', location),
        industry  = COALESCE((company_payload->>'industry')::demo.industry_enum, industry),
        employees = COALESCE((company_payload->>'employees')::INT, employees)
    WHERE company_id = target_company_id
    RETURNING * INTO updated_company;

    RETURN updated_company;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION demo.company_delete(target_company_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    deleted_count INT;
BEGIN
    DELETE FROM demo.companies WHERE company_id = target_company_id;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count > 0;
END;
$$ LANGUAGE plpgsql;
