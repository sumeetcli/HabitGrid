create table users (
    id integer primary key,
    username text unique not null,
    hash text not null
);

create table habits (
    id integer primary key,
    user_id integer not null,
    name text not null,
    created_at text not null
);

create table habit_logs (
    id integer primary key,
    habit_id integer not null,
    date text not null,
    done integer default 0
);