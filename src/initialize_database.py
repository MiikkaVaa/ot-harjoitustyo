from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS match_players;')
    cursor.execute('DROP TABLE IF EXISTS matches;')
    cursor.execute('DROP TABLE IF EXISTS players;')

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS players (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL UNIQUE,
                       rating INTEGER NOT NULL DEFAULT 1500
                   );
    ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS matches (
                       id INTEGER PRIMARY KEY,
                       team_a_points INTEGER NOT NULL,
                       team_b_points INTEGER NOT NULL
                   );
    ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS match_players (
                       match_id INTEGER NOT NULL REFERENCES matches(id),
                       player_name TEXT NOT NULL REFERENCES players(name),
                       team_side TEXT NOT NULL CHECK (team_side IN ("A", "B"))
                   );
    ''' )
    connection.commit()

def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

def ensure_database_initialized():
    connection = get_database_connection()

    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
