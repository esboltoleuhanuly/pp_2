-- Task 2: Insert or Update (Upsert)
CREATE OR REPLACE PROCEDURE upsert_phonebook(p_name VARCHAR, p_phone VARCHAR) AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE user_name = p_name) THEN
        UPDATE phonebook SET phone_number = p_phone WHERE user_name = p_name;
    ELSE
        INSERT INTO phonebook (user_name, phone_number) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Task 5: Delete by name or phone
CREATE OR REPLACE PROCEDURE delete_from_phonebook(p_target VARCHAR) AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE user_name = p_target OR phone_number = p_target;
END;
$$ LANGUAGE plpgsql;