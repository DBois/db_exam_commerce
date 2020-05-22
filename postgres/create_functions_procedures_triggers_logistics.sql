DROP FUNCTION IF EXISTS get_qty_of_product;
DROP PROCEDURE IF EXISTS add_employee, remove_employee, add_existing_item_to_stock, add_new_item_to_stock;

-- Functions


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

CREATE OR REPLACE PROCEDURE add_employee(p_name varchar, p_address varchar, p_salary int, p_job_position int, p_department int) 
	LANGUAGE plpgsql AS $$

	BEGIN 
		INSERT INTO employee (name, address, salary, job_position_fk, department_fk) 
		VALUES (p_name, p_address, p_salary, p_job_position, p_department);
	END
$$;

CREATE OR REPLACE PROCEDURE remove_employee(p_employee_id int) LANGUAGE plpgsql AS $$
	BEGIN 
		DELETE FROM employee WHERE id = p_employee_id;
	END
$$;


CREATE OR REPLACE PROCEDURE add_existing_item_to_stock(p_item_number varchar, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
	
	BEGIN 
		INSERT INTO department_item(item_fk, department_fk, qty) VALUES (p_item_number, p_department_number, p_qty);
	END
$$;



CREATE OR REPLACE PROCEDURE add_new_item_to_stock(p_product_number varchar, p_name varchar, p_description TEXT, p_price int, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
 	
	BEGIN
		INSERT INTO item(product_number, name, description, price) VALUES (p_product_number, p_name, p_description, p_price);
		INSERT INTO department_item(item_fk, department_fk, qty) VALUES (p_product_number, p_department_number, p_qty);
 	END
 $$;

-- Triggers

DROP TRIGGER IF EXISTS qty_couter ON department_item CASCADE;

CREATE TRIGGER qty_counter AFTER UPDATE ON department_item 
FOR EACH ROW EXECUTE FUNCTION restock_qty();
