from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.test import TestCreate, TestUpdate

import sqlite3

router = APIRouter()


@router.get("/all/{id_user}")
async def read_all_test_by_user(id_user: int):
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, power_max, hr_max, vo2_max, rf_max, cadence_max, date, id_test_type 
    FROM test
    WHERE id_user = ?;
    """

    cursor.execute(request)
    results = cursor.fetchall() # Récupération de tous les résultats dans une liste

    print(results) # Affichage des résultats

    # convertir les résultats en liste de dictionnaires
    convert_results = [list(t) for t in results]
    new_results = []

    for item in convert_results:
        convert_dict = {"id": item[0], "power_max": item[1], "hr_max": item[2], "vo2_max": item[3], "rf_max": item[4], "cadence_max": item[5], "date": item[6], "id_test": item[7]}
        new_results.append(convert_dict)
    
    print(new_results)

    conn.close() # Fermeture de la connexion
    return convert_results


@router.post("/add/{id_user}", response_model=TestCreate)
async def create_test_by_user(id_user: int, input_test: TestCreate):
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
