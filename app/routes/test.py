from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.test import TestCreate, TestUpdate

import sqlite3

router = APIRouter()


@router.get("/all/{id_user}")
async def read_all_test_by_user(id_user: int):
    """
    retourne tous les tests enregistrés par un utilisateur (id_user)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, power_max, hr_max, vo2_max, rf_max, cadence_max, date, id_test_type 
    FROM test
    WHERE id_user = ?;
    """

    cursor.execute(request, (id_user,))
    results = cursor.fetchall() # Récupération de tous les résultats dans une liste

    # convertir les résultats en liste de dictionnaires
    convert_results = [list(t) for t in results]
    new_results = []

    for item in convert_results:
        convert_dict = {"id": item[0], "power_max": item[1], "hr_max": item[2], "vo2_max": item[3], "rf_max": item[4], "cadence_max": item[5], "date": item[6], "id_test_type": item[7]}
        new_results.append(convert_dict)

    conn.close() # Fermeture de la connexion
    return convert_results


@router.post("/add/{id_user}")
async def create_test_by_user(id_user: int, input_test: TestCreate):
    """
    Enregistrement d'un test pour un utilisateur (id_user)
    """
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    power_max = input_test.power_max
    hr_max = input_test.hr_max
    vo2_max = input_test.vo2_max
    rf_max = input_test.rf_max
    cadence_max = input_test.cadence_max
    id_test_type = input_test.id_test_type

    request = """
    INSERT INTO test (power_max, hr_max, vo2_max, rf_max, cadence_max, id_test_type, id_user)
    VALUES (?, ?, ?, ?, ?, ?, ?);"""

    cursor.execute(request, (power_max, hr_max, vo2_max, rf_max, cadence_max, id_test_type, id_user))
    conn.commit()
    conn.close()


@router.patch("/update/{id_user}")
async def update_caracteristic(id_user: int, update_test: TestUpdate):
    """
    Mettre à jour le test d'un utilisateur (id_user) en fonction de l'id du test
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    id = update_test.id
    power_max = update_test.power_max
    hr_max = update_test.hr_max
    vo2_max = update_test.vo2_max
    rf_max = update_test.rf_max
    cadence_max = update_test.cadence_max
    id_test_type = update_test.id_test_type

    request = """
    UPDATE test 
    SET power_max = ?, hr_max = ?, vo2_max = ?, rf_max = ?, cadence_max = ?, id_test_type = ?
    WHERE id_user = ? AND id = ?;
    """

    cursor.execute(request, (power_max, hr_max, vo2_max, rf_max, cadence_max, id_test_type, id_user, id))
    conn.commit()
    conn.close()


@router.delete("/delete/{id_test}")
async def delete_user(id_test:int):
    """
    Supprime le test en fonction de son id
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    DELETE FROM test 
    WHERE id = ?;
    """

    cursor.execute(request, (id_test,))
    conn.commit()
    conn.close()


#Performance générale

@router.get("/best_power")
async def read_best_average_power():
    """
    retourne l'utilisateur avec la puissance max (power_max) la plus élevée en moyenne.
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT user.id, user.pseudo, user.email, AVG(test.power_max) AS avg_power_max
    FROM user
    JOIN test ON user.id = test.id_user
    GROUP BY user.id
    ORDER BY avg_power_max DESC
    LIMIT 1;
    """

    cursor.execute(request)
    result = cursor.fetchone() # Récupération de tous les résultats dans une liste
    conn.close()
    return result


@router.get("/best_vo2_max")
async def read_best_vo2_max():
    """
    retourne l'utilisateur ayant la vo2_max la plus élevé.
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT user.id, user.pseudo, user.email, MAX(test.vo2_max) AS max_vo2_max
    FROM user
    JOIN test ON user.id = test.id_user
    GROUP BY user.id
    ORDER BY max_vo2_max DESC
    LIMIT 1;
    """

    cursor.execute(request)
    result = cursor.fetchone() # Récupération de tous les résultats dans une liste
    conn.close()
    return result


@router.get("/best_ratio_weight_power")
async def read_best_ratio_weight_power():
    """
    retourne l'utilisateur ayant le meilleur ratio poids (weight) et puissance (power_max)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT u.id, u.pseudo, u.email, 
       AVG(t.power_max) / c.weight AS power_to_weight_ratio
    FROM user u
    JOIN test t ON u.id = t.id_user
    JOIN caracteristic c ON u.id = c.id_user
    GROUP BY u.id
    ORDER BY power_to_weight_ratio DESC
    LIMIT 1;
    """

    cursor.execute(request)
    result = cursor.fetchone() # Récupération de tous les résultats dans une liste
    conn.close()
    return result