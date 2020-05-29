DROP FUNCTION IF EXISTS get_qty_of_product, check_qty CASCADE;
DROP PROCEDURE IF EXISTS add_employee, remove_employee, add_existing_product_to_stock, add_new_product_to_stock;
DROP TRIGGER IF EXISTS qty_couter ON department_product CASCADE;

-- Functions

CREATE OR REPLACE FUNCTION check_qty() RETURNS TRIGGER 
	LANGUAGE plpgsql AS $$
	
	DECLARE 
		int_department_fk integer;
		var_product_fk varchar;
		int_qty int;
	
	BEGIN 
		SELECT department_fk, product_fk, qty INTO int_department_fk, var_product_fk, int_qty FROM department_product dp WHERE dp.qty <= 10;
	
		IF var_product_fk IS NOT NULL THEN
			RAISE NOTICE 'Product number: %, in Department: %, is running low! ', var_product_fk, int_department_fk;
		END IF;
	
		RETURN NEW;
	END
$$;

CREATE OR REPLACE FUNCTION get_qty_of_product(product_name varchar, product_number varchar DEFAULT '') 
 RETURNS TABLE (p_product_name varchar(64), p_product_fk varchar(30), p_department_fk int, p_qty int ) LANGUAGE plpgsql AS $$

BEGIN 
	IF product_number = '' THEN
	
		-- Searching on product name
		RETURN QUERY SELECT product.name, dp.* FROM product 
			JOIN department_product dp ON dp.product_fk = product.product_number
			WHERE name ILIKE '%' || product_name || '%';
	
	ELSE
	
		-- Searching on product number
		RETURN QUERY SELECT p.name, dp.* FROM department_product dp 
			JOIN product p ON p.product_number = dp.product_fk 
			WHERE dp.product_fk = product_number;

	END IF;

END
$$;

CREATE OR REPLACE FUNCTION get_qty_of_product_in_department(product_name varchar, department_id int, product_number varchar DEFAULT '')
	RETURNS TABLE (p_product_name varchar(64), p_product_fk varchar(30), p_department_fk int, p_qty int ) LANGUAGE plpgsql AS $$
	
BEGIN
		
	IF product_number = '' THEN
	
		-- Searching on product name
		RETURN QUERY SELECT product.name, dp.* FROM product 
			JOIN department_product dp ON dp.product_fk = product.product_number
			WHERE product.name ILIKE '%' || product_name || '%' AND dp.department_fk = department_id;
		
	ELSE
	
		-- Searching on product number
		RETURN QUERY SELECT p.name, dp.* FROM department_product dp 
			JOIN product p ON p.product_number = dp.product_fk 
			WHERE dp.product_fk = product_number AND dp.department_fk = department_id;

	END IF;
		
END
$$;

-- Procedures

CREATE OR REPLACE PROCEDURE restock_product(p_product_number varchar, p_department_number int, p_qty int) LANGUAGE plpgsql AS $$
	
	DECLARE 

		current_qty int;

	BEGIN
		IF p_qty < 0 THEN
			RAISE NOTICE 'You can not add a negative quantity amount to the stock';
		ELSE 
			SELECT qty INTO current_qty FROM department_product dp 
			WHERE product_fk = p_product_number AND department_fk = p_department_number;
		
			UPDATE department_product SET qty = (current_qty + p_qty) 
			WHERE product_fk = p_product_number AND department_fk = p_department_number;
		
			IF (SELECT EXISTS(SELECT 1 FROM department_product WHERE product_fk = p_product_number AND department_fk = p_department_number)) THEN 
				-- logging
				INSERT INTO restock_logfile(department_id, product_product_no, description) 
				VALUES (p_department_number, p_product_number, 
				format('Product number: %s, in Department: %s, has been restocked with %s products', p_product_number, p_department_number,  p_qty));
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


CREATE OR REPLACE PROCEDURE add_existing_product_to_stock(p_product_number varchar, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
	
	BEGIN 
		INSERT INTO department_product(product_fk, department_fk, qty) VALUES (p_product_number, p_department_number, p_qty);
	
		EXCEPTION
			WHEN SQLSTATE '23503' THEN 
				RAISE NOTICE 'Product number: % or department number: %, does not exist', p_product_number, p_department_number;
			WHEN OTHERS THEN
				RAISE NOTICE '% %', SQLERRM, SQLSTATE;
				
	END	
$$;



CREATE OR REPLACE PROCEDURE add_new_product_to_stock(p_product_number varchar, p_name varchar, p_description TEXT, p_price int, p_department_number int, p_qty int) 
	LANGUAGE plpgsql AS $$
 	
	BEGIN
		INSERT INTO product(product_number, name, description, price) VALUES (p_product_number, p_name, p_description, p_price);
		INSERT INTO department_product(product_fk, department_fk, qty) VALUES (p_product_number, p_department_number, p_qty);
 	
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

CREATE TRIGGER qty_counter AFTER UPDATE ON department_product 
FOR EACH ROW EXECUTE FUNCTION check_qty();
