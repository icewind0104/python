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
    unique key `index_switch_indicator` (`switch_id`, `name`),
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