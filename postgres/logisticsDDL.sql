drop table if exists department_item, employee, item, department, job_position

create table department
(
    id      serial       not null
        constraint department_pk
            primary key,
    address varchar(255) not null,
    name    varchar(64)  not null
);

create table job_position
(
    id    serial      not null
        constraint job_position_pk
            primary key,
    title varchar(64) not null
);
create table item
(
    id             bigserial   not null
        constraint item_pk
            primary key,
    product_number varchar(30) not null,
    name           varchar(64) not null,
    description    text        not null,
    price          integer     not null
);

create table department_item
(
    "item_FK"       bigserial not null
        constraint department_item_item_id_fk
            references item,
    "department_FK" serial    not null
        constraint department_item_department_id_fk
            references department,
    qty             integer
);

create table employee
(
    id                serial       not null
        constraint employee_pk
            primary key,
    name              varchar(128) not null,
    address           varchar(255) not null,
    salary            integer      not null,
    "job_position_FK" integer      not null
        constraint employee_job_position_id_fk
            references job_position,
    "department_FK"   integer      not null
        constraint employee_department_id_fk
            references department
);
