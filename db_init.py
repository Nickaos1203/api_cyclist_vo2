import sqlite3

# Création de tables sur sqlite
def create_user_table():
    """
    Création de la table 'user' dans la base de données
    avec les valeurs suivantes :
    - id : identifiant unique,
    - pseudo : pseudonyme unique,
    - email : email unique,
    - password : mot de passe, 
    - is_coach : profil de l'utilisateur avec les valeurs 0 (non coach) et 1 (coach)
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    request = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        pseudo TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_coach NUMERIC NOT NULL
    );
    """
    cursor.execute(request)
    conn.commit()
    conn.close()


def create_caracteristic_table():
    """
    Création de la table 'caracteristic' dans la base de données
    avec les valeurs suivantes :
    - gender : genre de l'utilisateur avec les valeurs 1 (homme) et 2 (femme),
    - age : âge de l'utilisateur,
    - weight : poids de l'utilisateur en kg,
    - height : taille de l'utilisateur en cm, 
    - id_user : l'identifiant unique de l'utilisateur
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    request = """
    CREATE TABLE IF NOT EXISTS caracteristic (
        gender INTEGER NOT NULL,
        age INTEGER NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        id_user INTEGER NOT NULL UNIQUE,
        FOREIGN KEY(id_user) REFERENCES user(id) ON DELETE CASCADE
    );
    """
    cursor.execute(request)
    conn.commit()
    conn.close()


def create_test_type_table():
    """
    Création de la table 'test_type' dans la base de données
    avec les valeurs suivantes :
    - id : identifiant unique,
    - name_type : nom du type de test
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    request = """
    CREATE TABLE IF NOT EXISTS test_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_type TEXT NOT NULL UNIQUE
    );
    """
    cursor.execute(request)
    conn.commit()
    conn.close()


def create_test_table():
    """
    Création de la table 'test' dans la base de données
    avec les valeurs suivantes :
    - id : identifiant unique,
    - power_max : puissance maximale,
    - hr_max : hr max,
    - vo2_max : VO2 max, 
    - rf_max : rf max,
    - cadence_max : cadence maximale,
    - date : date du test
    - id_user : l'identifiant de l'utilisateur ayant effectué le test
    - id_test_type : identifiant du nom du test
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    request = """
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        power_max REAL NOT NULL,
        hr_max REAL NOT NULL,
        vo2_max REAL NOT NULL,
        rf_max REAL NOT NULL,
        cadence_max REAL NOT NULL,
        date DATE DEFAULT (DATE('now')),
        id_user INTEGER NOT NULL,
        id_test_type INTEGER NOT NULL,
        FOREIGN KEY(id_user) REFERENCES user(id) ON DELETE CASCADE,
        FOREIGN KEY(id_test_type) REFERENCES test_type(id)
    );
    """
    cursor.execute(request)
    conn.commit()
    conn.close()


# Create all tables in the database
def create_tables():
    create_user_table()
    create_caracteristic_table()
    create_test_type_table()
    create_test_table()


create_tables()