-- Migrations will appear here as you chat with AI

create table organization (
  id bigint primary key generated always as identity,
  name text not null,
  domain text not null,
  description text,
  image text
);

create table team (
  id bigint primary key generated always as identity,
  name text not null,
  description text,
  organizationid bigint references organization (id)
);

create table member (
  id bigint primary key generated always as identity,
  teamid bigint references team (id),
  firstname text not null,
  lastname text not null,
  rol text not null,
  roldescription text,
  gender text
);

create table users (
  id bigint primary key generated always as identity,
  firstname text not null,
  lastname text not null,
  avatar text,
  organizationid bigint references organization (id)
);

create table integration (
  id bigint primary key generated always as identity,
  title text not null,
  name text not null,
  organizationid bigint references organization (id),
  ownerid bigint references users (id),
  token text
);

alter table member
drop constraint member_teamid_fkey;

alter table member
rename column teamid to organizationid;

alter table member
add constraint member_organizationid_fkey foreign key (organizationid) references organization (id);

drop table team;

alter table member
add column userid bigint;

alter table member
add constraint member_userid_fkey foreign key (userid) references users (id);

alter table member
rename column firstname to first_name;

alter table member
rename column lastname to last_name;

alter table member
rename column rol to role;

alter table member
rename column roldescription to role_description;

alter table member
rename column organizationid to organization_id;

alter table member
rename column userid to user_id;

alter table users
rename column firstname to first_name;

alter table users
rename column lastname to last_name;

alter table users
rename column organizationid to organization_id;

alter table integration
rename column organizationid to organization_id;

alter table integration
rename column ownerid to owner_id;

create table agents (
  id bigint primary key generated always as identity,
  name text not null,
  organization_id bigint references organization (id),
  enabled boolean default true
);

create table platform (
  id bigint primary key generated always as identity,
  name text not null,
  description text
);
