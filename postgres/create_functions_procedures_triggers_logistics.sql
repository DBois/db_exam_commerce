
-- Functions

DROP FUNCTION IF EXISTS get_qty_of_product;

CREATE OR REPLACE FUNCTION get_qty_of_product(item_name varchar, item_number varchar DEFAULT '') 
 RETURNS TABLE (p_item_name varchar(64), p_item_fk varchar(30), p_department_fk int, p_qty int ) LANGUAGE plpgsql AS $$

BEGIN 
	IF item_number = '' THEN
	
		-- Searching on item name
		RETURN QUERY SELECT item.name, di.* FROM item 
			JOIN department_item di ON di.item_fk = item.product_number
			WHERE name ILIKE '%' || item_name || '%';
	
	ELSE
	
		-- Searching on product number
		RETURN QUERY SELECT i.name, di.* FROM department_item di 
			JOIN item i ON i.product_number = di.item_fk 
			WHERE di.item_fk = item_number;

	END IF;

END;
$$

CREATE OR REPLACE FUNCTION get_qty_of_product_in_department(item_name varchar, department_id int, item_number varchar DEFAULT '')
	RETURNS TABLE (p_item_name varchar(64), p_item_fk varchar(30), p_department_fk int, p_qty int ) LANGUAGE plpgsql AS $$
	
BEGIN
		
	IF item_number = '' THEN
	
		-- Searching on item name
		RETURN QUERY SELECT item.name, di.* FROM item 
			JOIN department_item di ON di.item_fk = item.product_number
			WHERE item.name ILIKE '%' || item_name || '%' AND di.department_fk = department_id;
	
	ELSE
	
		-- Searching on product number
		RETURN QUERY SELECT i.name, di.* FROM department_item di 
			JOIN item i ON i.product_number = di.item_fk 
			WHERE di.item_fk = item_number AND di.department_fk = department_id;

	END IF;
		
END
$$;

-- Procedures

-- Triggers

DROP TRIGGER IF EXISTS qty_couter ON department_item CASCADE;

CREATE TRIGGER qty_counter AFTER UPDATE ON department_item 
FOR EACH ROW EXECUTE FUNCTION restock_qty();
