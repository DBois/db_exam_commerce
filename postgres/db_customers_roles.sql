drop owned by administrator, readonly, customer_support;
drop role if exists administrator, readonly, customer_support;
drop user if exists admin_user, readonly_user, cs_user;


-- Create role
create role administrator;
create role readonly;
create role customer_support;


-- Creater user
create user admin_user with encrypted password 'admin';
create user readonly_user with encrypted password 'readonly';
create user cs_user with encrypted password 'cs';


-- Assign role to user
grant administrator to admin_user;
grant readonly to readonly_user;
grant customer_support to cs_user;






grant connect on database db_exam_customers to administrator, readonly, customer_support;

-- Admin access
GRANT ALL PRIVILEGES ON ALL TABLES in schema public to administrator;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO administrator;

-- Readonly access
grant select on all tables in schema public to readonly;

-- Customer support access
grant select, update on all sequences in schema public to customer_support;
grant insert, select, update on all tables in schema public to customer_support;