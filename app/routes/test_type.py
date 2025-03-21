from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.test import TestTypeCreate

import sqlite3

router = APIRouter()

# Test_type routes

@router.get("/")
async def read_all_test_names():
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, name_type FROM test_type
    """

    cursor.execute(request)
    results = cursor.fetchall() # Récupération de tous les résultats dans une liste

    print(results) # Affichage des résultats

    # convertir les résultats en liste de dictionnaires
    convert_results = [list(t) for t in results]
    new_results = []

    for item in convert_results:
        convert_dict = {"id": item[0], "name_type": item[1]}
        new_results.append(convert_dict)
    
    print(new_results)

    conn.close() # Fermeture de la connexion
    return convert_results


@router.post("/add", response_model=TestTypeCreate)
async def create_test_type(input_test_type: TestTypeCreate):
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    name_type = input_test_type.name_type

    request = """
    INSERT INTO test_type (name_type)
    VALUES (?);"""

    cursor.execute(request, (name_type,))
    conn.commit()
    conn.close()


@router.delete("/{id}")
async def delete_user(id: int):
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    DELETE FROM test_type 
    WHERE id = ?;
    """

    cursor.execute(request, (id,))
    conn.commit()
    conn.close()

