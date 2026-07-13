create table users (
    id integer primary key,
    username text unique not null,
    hash text not null
);

create table habits (
    id integer primary key,
    user_id integer not null,
    name text not null
);

create table habit_logs (
    id integer primary key,
    habit_id integer not null,
    date text not null,
    done integer not null default 0
);

create table journal (
    id integer primary key,
    user_id integer not null,
    date text not null,
    entry text
);

create table settings (
    user_id integer primary key,
    theme text default 'Dark',
    default_view text default 'Overall',
    journal_template text,
    dob text,
    country text
);