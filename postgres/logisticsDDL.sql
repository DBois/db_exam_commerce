drop table if exists department_item, employee, job_position, department, item, restock_logfile;

create table department
(
    id      serial       not null
        constraint department_pk
            primary key,
    address varchar(255) not null,
    name    varchar(64)  not null
);

alter table department
    owner to postgres;

create table job_position
(
    id    serial      not null
        constraint job_position_pk
            primary key,
    title varchar(64) not null
);

alter table job_position
    owner to postgres;

create table item
(
    product_number varchar(30) not null
        constraint item_pk
            primary key,
    name           varchar(64) not null,
    description    text        not null,
    price          integer     not null
);

alter table item
    owner to postgres;

create table employee
(
    id                serial       not null
        constraint employee_pk
            primary key,
    name              varchar(128) not null,
    address           varchar(255) not null,
    salary            integer      not null,
    "job_position_fk" integer      not null
        constraint employee_job_position_id_fk
            references job_position,
    "department_fk"   integer      not null
        constraint employee_department_id_fk
            references department
);

alter table employee
    owner to postgres;

create table department_item
(
    item_fk       varchar(30) not null,
    department_fk integer     not null,
    qty           integer     not null,
    constraint pf primary key (item_fk, department_fk),
    constraint department_item_item_product_number_fk foreign key (item_fk) references item,
    constraint department_item_department_id_fk foreign key (department_item) references department,
);

alter table department_item
    owner to postgres;

create table restock_logfile
(
    department_id   integer,
    item_product_no varchar(30),
    description     text,
    logged_at       timestamp default CURRENT_TIMESTAMP
);

alter table restock_logfile
    owner to postgres;

