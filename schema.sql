drop database if exists monitor;

create database monitor;

use monitor;

create table users(
    `id` integer not null auto_increment,
    `name` varchar(50) not null,
    `passwd` varchar(50) not null,
    `level` int not null,
    unique key `index_name` (`name`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table switches(
    `id` integer not null auto_increment,
    `name` varchar(50),
    `vendor` varchar(50) not null,
    `model` varchar(50) not null,
    `host` varchar(50) not null,
    `user` varchar(50),
    `password` varchar(50),
    `supassword` varchar(50),
    `snmp_community` varchar(50),
    `snmp_version` varchar(50),
    unique key `index_host` (`host`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table indicator(
    `id` integer not null auto_increment,
    `switch_id` int not null,
    `name` varchar(50) not null,
    `argument` varchar(50) not null,
    `title` varchar(50),
    foreign key (`switch_id`) references switches(`id`),
    unique key `indicator` (`switch_id`, `name`,`argument`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table quick_indicator(
    `id` integer not null auto_increment,
    `switch_id` int not null,
    `host` varchar(50) not null,
    `name` varchar(50),
    `cpu` varchar(50),
    `memory` varchar(50),
    foreign key (`switch_id`) references switches(`id`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table switches_groups(
    `id` integer not null auto_increment,
    `switch_id` int not null,
    `group_id` int not null,
    foreign key (`switch_id`) references switches(`id`),
    foreign key (`group_id`) references groups(`id`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table groups(
    `id` integer not null auto_increment,
    `name` varchar(50) not null,
    `priority` integer,
    `category_id` integer,
    foreign key (`category_id`) references category(`id`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table category(
    `id` integer not null auto_increment,
    `name` varchar(50) not null,
    primary key (`id`)
) engine=innodb default charset=utf8;
