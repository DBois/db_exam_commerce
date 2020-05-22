DROP function IF EXISTS restock_qty cascade;
DROP TRIGGER IF EXISTS qty_couter ON department_item CASCADE;

CREATE OR REPLACE FUNCTION public.restock_qty()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE 
	int_department_fk integer;
	var_item_fk varchar;

BEGIN 
	SELECT department_fk, item_fk INTO int_department_fk, var_item_fk FROM department_item di WHERE di.qty <= 2;
	UPDATE department_item SET qty = 100 WHERE item_fk = var_item_fk AND department_fk = int_department_fk;
	
	IF int_department_fk IS NOT NULL THEN 
		-- logging
		INSERT INTO restock_logfile(department_id, item_product_no, description) VALUES (int_department_fk, var_item_fk, 'Restocked');
	END IF;

	RETURN NEW;

END;
$function$ ;

CREATE TRIGGER qty_counter AFTER UPDATE ON department_item 
FOR EACH ROW EXECUTE FUNCTION restock_qty();
