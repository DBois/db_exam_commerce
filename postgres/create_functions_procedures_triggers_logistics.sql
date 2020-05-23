DROP FUNCTION IF EXISTS get_qty_of_product, check_qty CASCADE;
DROP PROCEDURE IF EXISTS add_employee, remove_employee, add_existing_item_to_stock, add_new_item_to_stock;
DROP TRIGGER IF EXISTS qty_couter ON department_item CASCADE;

-- Functions

CREATE OR REPLACE FUNCTION check_qty() RETURNS TRIGGER 
	LANGUAGE plpgsql AS $$
	
	DECLARE 
		int_department_fk integer;
		var_item_fk varchar;
		int_qty int;
	
	BEGIN 
		SELECT department_fk, item_fk, qty INTO int_department_fk, var_item_fk, int_qty FROM department_item di WHERE di.qty <= 2;
	
		IF var_item_fk IS NOT NULL THEN
			RAISE NOTICE 'Product number: %, in Department: %, is running low! ', var_item_fk, int_department_fk;
		END IF;
	
		RETURN NEW;
	END
$$;

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

END
$$;

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

CREATE OR REPLACE PROCEDURE restock_item(p_product_number varchar, p_department_number int, p_qty int) LANGUAGE plpgsql AS $$
	
	DECLARE 

		current_qty int;

	BEGIN
		IF p_qty < 0 THEN
			RAISE NOTICE 'You can not add a negative quantity amount to the stock';
		ELSE 
			SELECT qty INTO current_qty FROM department_item di 
			WHERE item_fk = p_product_number AND department_fk = p_department_number;
		
			UPDATE department_item SET qty = (current_qty + p_qty) 
			WHERE item_fk = p_product_number AND department_fk = p_department_number;
		
			IF (SELECT EXISTS(SELECT 1 FROM department_item WHERE item_fk = p_product_number AND department_fk = p_department_number)) THEN 
				-- logging
				INSERT INTO restock_logfile(department_id, item_product_no, description) 
				VALUES (p_department_number, p_product_number, 
				format('Product number: %s, in Department: %s, has been restocked with %s items', p_product_number, p_department_number,  p_qty));
			END IF;
		END IF;
		
	
		-- Update on incorret fk's dose not throw an exception to catch
		
	END
$$;

CREATE OR REPLACE PROCEDURE add_employee(p_name varchar, p_address varchar, p_salary int, p_job_position int, p_department int) 
	LANGUAGE plpgsql AS $$

	BEGIN 
		INSERT INTO employee (name, address, salary, job_position_fk, department_fk) 
		VALUES (p_name, p_address, p_salary, p_job_position, p_department);
	
		EXCEPTION
			WHEN SQLSTATE '23503' THEN 
				RAISE NOTICE 'Job position id: % or department number: %, does not exist', p_job_position, p_department;
			WHEN OTHERS THEN
				RAISE NOTICE '% %', SQLERRM, SQLSTATE;
	END
$$;

CREATE OR REPLACE PROCEDURE remove_employee(p_employee_id int) LANGUAGE plpgsql AS $$
	BEGIN 
		DELETE FROM employee WHERE id = p_employee_id;
		-- Delete on incorrect id dose not throw an exception to catch
	END
$$;


CREATE OR REPLACE PROCEDURE add_existing_item_to_stock(p_item_number varchar, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
	
	BEGIN 
		INSERT INTO department_item(item_fk, department_fk, qty) VALUES (p_item_number, p_department_number, p_qty);
	
		EXCEPTION
			WHEN SQLSTATE '23503' THEN 
				RAISE NOTICE 'Product number: % or department number: %, does not exist', p_item_number, p_department_number;
			WHEN OTHERS THEN
				RAISE NOTICE '% %', SQLERRM, SQLSTATE;
				
	END	
$$;



CREATE OR REPLACE PROCEDURE add_new_item_to_stock(p_product_number varchar, p_name varchar, p_description TEXT, p_price int, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
 	
	BEGIN
		INSERT INTO item(product_number, name, description, price) VALUES (p_product_number, p_name, p_description, p_price);
		INSERT INTO department_item(item_fk, department_fk, qty) VALUES (p_product_number, p_department_number, p_qty);
 	
 		EXCEPTION
 			WHEN SQLSTATE '23505' THEN
 				RAISE NOTICE 'Product number: % already exist', p_product_number;
			WHEN SQLSTATE '23503' THEN 
				RAISE NOTICE 'Department number: %, does not exist', p_department_number;
			WHEN OTHERS THEN
				RAISE NOTICE '% %', SQLERRM, SQLSTATE;
 	
 	END
 $$;

-- Triggers

CREATE TRIGGER qty_counter AFTER UPDATE ON department_item 
FOR EACH ROW EXECUTE FUNCTION check_qty();
