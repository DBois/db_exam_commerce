drop table if exists credit_card, customer;

create table customer
(
    id           bigserial    not null
        constraint customer_pk
            primary key,
    name         varchar(64)  not null,
    email        varchar(64)  not null,
    password     varchar(255) not null,
    address      varchar(255),
    phone_number varchar(15)
);


create table credit_card
(
    card_number     varchar(16) not null,
    expiration_date varchar(4)  not null,
    "customer_FK"   bigserial   not null
        constraint credit_card_customer_id_fk
            references customer
);
