drop function if exists get_employees;
create or replace function get_employees(department_id int)
returns table (
    id int,
	name VARCHAR,
	salary int,
	address VARCHAR,
	title VARCHAR,
	dept_id int
)
as $$
BEGIN
return query select e.id, e.name, e.salary, e.address, jp.title, e.department_fk 
from employee e join job_position jp 
on e.job_position_fk  = jp.id where e.department_fk = department_id;
end; $$
language 'plpgsql';