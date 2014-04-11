drop table if exists pictures;
create table pictures (
  id integer primary key autoincrement,
  title text not null,
  caption text,
  category text,
  url text,
  date date
);