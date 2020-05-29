--drop owned by administrator, read_only, customer_support, hr, department_manager, dm_user;
drop role if exists administrator, read_only, customer_support, hr, department_manager;
drop user if exists admin_user, read_only_user, cs_user, hr_user, dm_user;

-- Create role
create role administrator;
create role read_only;
create role customer_support;
create role hr;
create role department_manager;

-- Creater user
create user admin_user with encrypted password 'admin';
create user read_only_user with encrypted password 'readonly';
create user cs_user with encrypted password 'cs';
create user hr_user with encrypted password 'hr';
create user dm_user with encrypted password 'dm';

-- Assign role to user
grant administrator to admin_user;
grant read_only to read_only_user;
grant customer_support to cs_user;
grant hr to hr_user;
grant department_manager to dm_user;

-- Grant access to DBs
grant connect on database db_exam_customers to administrator, read_only, customer_support;
grant connect on database db_exam_logistics to customer_support, hr, dm_user;

-- Admin access
GRANT ALL PRIVILEGES ON ALL TABLES in schema public TO  administrator;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO administrator;

-- read_only access
grant select on all tables in schema public to read_only;

-- Customer support access
grant select, update on all sequences in schema public to customer_support;
grant insert, select, update on all tables in schema public to customer_support;
grant select on product to customer_support;
GRANT SELECT ON restock_logfile TO customer_support;
-- HR access
grant select on department to hr;
grant all privileges on employee, job_position to hr;
grant all privileges on all sequences in schema public to hr;

-- Department manager
grant all privileges on department_product to department_manager;
grant select, update on department to department_manager;
grant insert, select on product to department_manager;
GRANT SELECT ON restock_logfile TO department_manager;

