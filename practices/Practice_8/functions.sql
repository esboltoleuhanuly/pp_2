-- Task 1: Search by pattern (Matches name or phone)
CREATE OR REPLACE FUNCTION get_users_by_pattern(p_pattern TEXT)
RETURNS TABLE(u_name VARCHAR, u_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT user_name, phone_number 
    FROM phonebook 
    WHERE user_name ILIKE '%' || p_pattern || '%' 
       OR phone_number ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- Task 4: Pagination
CREATE OR REPLACE FUNCTION get_users_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(u_name VARCHAR, u_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT user_name, phone_number 
    FROM phonebook 
    ORDER BY user_name 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;