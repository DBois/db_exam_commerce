drop table if exists customer_credit_card, credit_card, customer;

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
    card_number     char(16)     not null,
    expiration_date char(4)      not null,
    name            varchar(255) not null,
    constraint credit_card_pkey
        primary key (card_number, expiration_date)
);

create unique index credit_card_card_number_uindex
    on credit_card (card_number);

create unique index credit_card_expiration_date_uindex
    on credit_card (expiration_date);

create table customer_credit_card
(
    customer_fk                 integer
        constraint customer_credit_card_customer_id_fk
            references customer,
    credit_card_number          char(16) not null,
    credit_card_expiration_date char(4)  not null,
    constraint customer_credit_card_credit_card_card_number_expiration_date_fk
        foreign key (credit_card_number, credit_card_expiration_date) references credit_card
);

