drop table if exists department_product, employee, job_position, department, product, restock_logfile;

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

create table product
(
    product_number varchar(30) not null
        constraint product_pk
            primary key,
    name           varchar(64) not null,
    description    text        not null,
    price          integer     not null
);

alter table product
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

create table department_product
(
    product_fk       varchar(30) not null,
    department_fk integer     not null,
    qty           integer     not null,
    constraint pf primary key (product_fk, department_fk),
    constraint department_product_product_product_number_fk foreign key (product_fk) references product,
    constraint department_product_department_id_fk foreign key (department_product) references department,
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

