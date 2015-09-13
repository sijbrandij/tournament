#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    result = c.fetchone()
    db.close()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s)", (bleach.clean(name),))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("select * from standings")
    results = c.fetchall()
    standings = []
    for player in results:
        c.execute("select id from players where name = %s", [player[0]])
        player_id = c.fetchone()
        ## get the player
        c.execute("select num from number_of_wins where name = %s", [player[0]])
        player_wins = c.fetchone()
        ## get the player's number of wins
        c.execute("select num from number_of_matches where name = %s", [player[0]])
        player_matches = c.fetchone()
        ## get the player's number of matches
        standings.append((player_id[0], player[0], player_wins[0], player_matches[0]))
        ## add player to the standings with their id, name, number of wins and number of matches
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches values (%s, %s)", [winner, loser])
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    swiss_pairings = []
    c.execute("select * from players")
    players = c.fetchall()
    ## get all players
    for player in players:
        c.execute("select num from number_of_wins where name = %s", [player[1]])
        number_of_wins = c.fetchone()
        ## get the player's number of wins
        c.execute("select * from number_of_wins where name != %s and num = %s", [player[1], number_of_wins[0]])
        player2_name = c.fetchone()
        ## get a player with an equal number of wins which is not the first player
        c.execute("select * from players where name = %s", [player2_name[0]])
        player2 = c.fetchone()
        ## get the second player's name
        players.remove(player)
        players.remove(player2)
        ## remove players from players list because they have been paired up
        swiss_pairings.append((player[0], player[1], player2[0], player2[1]))
        ## add the pair to the list of pairings
    db.close
    return swiss_pairings
