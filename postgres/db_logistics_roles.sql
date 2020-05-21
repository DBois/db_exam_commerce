drop owned by hr, department_manager;
drop role if exists hr, department_manager;
drop user if exists hr_user, dm_user;

-- Create role
create role hr;
create role department_manager;

-- Create user
create user hr_user with encrypted password 'hr';
create user dm_user with encrypted password 'dm';


-- Assign role to user
grant hr to hr_user;
grant department_manager to dm_user;

grant connect on database db_exam_logistics to customer_support, hr, dm_user;

-- Admin access
GRANT ALL PRIVILEGES ON ALL TABLES in schema public to administrator;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO administrator;

-- Readonly access
grant select on all tables in schema public to readonly;

-- Customer support access
grant select on item to customer_support;

-- HR access
grant select on department to hr;
grant all privileges on employee, job_position to hr;
grant all privileges on all sequences in schema public to hr;

-- Department manager
grant all privileges on department_item to department_manager;
grant select, update on department to department_manager;
grant insert, select on item to department_manager;