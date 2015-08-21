# Tournament
This code includes the setup of a database scheme to store the game matches between players, plus a Pyhton module to rank the players and pair the players up in a tournament using the Swiss system (each player should be paired with another player with the same number of wins, or as close as possible).

## Author
[Karen Sijbrandij] (https://github.com/sijbrandij)

## System requirements
1. PostgreSQL
2. Python

## Setup
1. start a postgresql console by typing ```psql``` in a terminal
2. Go to the tournament folder on your system
3. setup the database, tables and switch to this database by typing ```\i tournament.sql```

## Test instructions
To run the tests, run
```
python tournament_test.py
```
