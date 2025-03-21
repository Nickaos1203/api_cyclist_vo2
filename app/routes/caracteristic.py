from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.caracteristic import CaracteristicCreate, CaracteristicUpdate

import sqlite3

router = APIRouter()

@router.get("/")
async def read_all_caracteristics():
    """
    retourne les caractéristiques de tous les utilisateurs
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, gender, age, weight, height, id_user FROM caracteristic;
    """

    cursor.execute(request)
    results = cursor.fetchall() # Récupération de tous les résultats dans une liste

    print(results) # Affichage des résultats

    # convertir les résultats en liste de dictionnaires
    convert_results = [list(t) for t in results]
    new_results = []

    for item in convert_results:
        convert_dict = {"id": item[0], "pseudo": item[1], "email": item[2], "password": item[3], "is_coach": item[4]}
        new_results.append(convert_dict)
    
    print(new_results)

    conn.close() # Fermeture de la connexion
    return convert_results


@router.get("/{id}")
async def read_caracteristic(id: int):
    """
    retourne les caractéristiques d'un utilisateur en fonction de son id
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, gender, age, weight, height, id_user FROM caracteristic
    WHERE id = ?;
    """

    cursor.execute(request, (id,))
    result = cursor.fetchone() # Récupération de tous les résultats dans une liste
    print(result)
    conn.close()
    return result


@router.post("/add")
async def create_caracteristic(create_caracteristic: CaracteristicCreate):
    """
    Ajoute des caractéristiques à un utilisateur en fonction de son id(id_user)
    """
    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    gender = create_caracteristic.gender
    age = create_caracteristic.age
    weight = create_caracteristic.weight
    height = create_caracteristic.height
    id_user = create_caracteristic.id_user

    request = """
    INSERT INTO caracteristic (gender, age, weight, height, id_user)
    VALUES (?, ?, ?, ?, ?);
    """

    cursor.execute(request, (gender, age, weight, height, id_user))
    conn.commit()
    conn.close()


@router.put("/update/{id_user}")
async def update_caracteristic(id_user: int, update_caracteristic: CaracteristicUpdate):
    """
    Mettre à jour les caractéristiques d'un utilisateur en fonction de son id
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    gender = update_caracteristic.gender
    age = update_caracteristic.age
    weight = update_caracteristic.weight
    height = update_caracteristic.height

    request = """
    UPDATE caracteristic 
    SET gender = ?, age = ?, weight = ?, height = ?
    WHERE id_user = ?;
    """

    cursor.execute(request, (genre, age, weight, height, id_user))
    conn.commit()
    conn.close()


@router.delete("/delete/{id_user}")
async def delete_caracteristic(id_user):
    """
    Supprime les caractéristiques d'un utilisateur en fonction de son id (id_user)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    DELETE FROM caracteristic 
    WHERE id_user = ?;
    """

    cursor.execute(request, (id_user,))
    conn.commit()
    conn.close()
