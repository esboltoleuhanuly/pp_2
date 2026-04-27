-- =============================================
-- TSIS 1: New Stored Procedures & Functions
-- Do NOT duplicate anything from Practice 8
-- =============================================

-- Task 3.4.1: Add a phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR  -- 'home' | 'work' | 'mobile'
) AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE user_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type "%". Use home, work, or mobile.', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$ LANGUAGE plpgsql;


-- Task 3.4.2: Move a contact to a group (creates the group if missing)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
) AS $$
DECLARE
    v_group_id   INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Get or create the group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;

    -- Verify contact exists
    SELECT id INTO v_contact_id FROM contacts WHERE user_name = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$ LANGUAGE plpgsql;


-- Task 3.4.3: Extended search — matches name, email, AND all phone numbers
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    u_name  VARCHAR,
    u_email VARCHAR,
    u_phone VARCHAR,
    u_type  VARCHAR,
    u_group VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.user_name,
        c.email,
        p.phone,
        p.type,
        g.name
    FROM contacts c
    LEFT JOIN phones  p ON p.contact_id = c.id
    LEFT JOIN groups  g ON g.id = c.group_id
    WHERE
        c.user_name ILIKE '%' || p_query || '%'
     OR c.email     ILIKE '%' || p_query || '%'
     OR p.phone     ILIKE '%' || p_query || '%'
    ORDER BY c.user_name;
END;
$$ LANGUAGE plpgsql;