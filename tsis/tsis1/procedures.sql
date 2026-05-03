-- Add new phone to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, LOWER(p_type))
    ON CONFLICT (contact_id, phone) DO NOTHING;
END;
$$;

-- Move contact to group (create group if needed)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;

-- Extended search by name/email/any phone
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id  INT,
    name        VARCHAR,
    email       VARCHAR,
    birthday    DATE,
    group_name  VARCHAR,
    phones      TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS contact_id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(
            STRING_AGG(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id),
            ''
        ) AS phones
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
       OR EXISTS (
            SELECT 1
            FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || p_query || '%'
       )
    GROUP BY c.id, c.name, c.email, c.birthday, g.name
    ORDER BY c.name;
END;
$$;