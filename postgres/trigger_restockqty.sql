DROP function IF EXISTS restock_qty cascade;
DROP TRIGGER IF EXISTS qty_couter ON department_item CASCADE;

create or replace function restock_qty() returns trigger as $$
declare 
	int_department_fk integer;
	var_item_fk varchar;

begin 
	select department_fk into int_department_fk from department_item di where di.qty <= 2;
	select item_fk into var_item_fk from department_item di where di.qty <= 2;

	-- TODO: Write to a log file
	update department_item set qty = 100 where item_fk = var_item_fk and department_fk = int_department_fk;
	
	return new;
end;
$$ language plpgsql;

create trigger qty_counter after update on department_item for each row execute procedure restock_qty();
