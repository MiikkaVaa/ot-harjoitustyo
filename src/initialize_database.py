from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
                   DROP TABLE IF EXISTS players;
    ''')

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
                   CREATE TABLE players (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL UNIQUE,
                       rating INTEGER NOT NULL DEFAULT 1500
                   );
    ''')

    connection.commit()

def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
