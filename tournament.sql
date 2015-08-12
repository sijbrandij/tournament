-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create database tournament;
-- create tournament database

\c tournament;
-- connect to the database

create table players(
    id serial primary key,
    name text
);
-- create players table containing an id and a name

create table matches(
  player1 integer references players (id),
  player2 integer references players (id),
  winner integer references players (id)
);
-- create matches table using player ids and registering the winning player's id

create view number_of_matches as
  select players.name, count(matches.winner) as num
  from matches right join players
  on matches.player1 = players.id or matches.player2 = players.id
  group by players.id
  order by players.name
;

create view number_of_wins as
  select players.name, count(matches.winner) as num
  from matches right join players
  on matches.winner = players.id
  group by players.id
  order by players.name
;

create view standings as
  select players.name, count(matches.winner) as num
  from matches right join players
  on matches.winner = players.id
  group by players.id
  order by num desc
;
