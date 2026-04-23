-- 1. Upsert (Insert or Update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Delete by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_search TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_search OR phone = p_search;
END;
$$;
