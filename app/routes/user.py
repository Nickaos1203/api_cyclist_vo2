from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, UserRead, UserUpdate, UserUpdatePassword

import sqlite3

router = APIRouter()


@router.get("/{id}")
async def read_user(id: int):
    """
    retourne un utilisateur en fonction de son id
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, pseudo, email, password, is_coach FROM user
    WHERE id = ?;
    """

    cursor.execute(request, (id,))
    result = cursor.fetchone() # Récupération de tous les résultats dans une liste
    print(result)
    conn.close()
    return result


@router.get("/")
async def read_user_all():
    """
    retourne tous les utilisateurs
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    SELECT id, pseudo, email, password, is_coach FROM user;
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


@router.patch("/update/{id_user}")
async def update_user(id_user: int, update_user: UserUpdate):
    """
    Mettre à jour des informations d'un utilisateur en fonction de son id (id_user)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    pseudo = update_user.pseudo
    email = update_user.email
    is_coach = update_user.is_coach


    request = """
    UPDATE user 
    SET pseudo = ?, email = ?, is_coach = ? 
    WHERE id = ?;
    """

    cursor.execute(request, (pseudo, email, is_coach, id_user))
    conn.commit()
    conn.close()


@router.patch("/update_password/{id_user}")
async def update_user_password(id_user: int, password_updated: UserUpdatePassword):
    """
    Mettre à jour le mot de passe d'un utlisateur en fonction de son id (id_user)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    password = password_updated.password

    request = """
    UPDATE user 
    SET password = ?
    WHERE id = ?;
    """

    cursor.execute(request, (password, id_user))
    conn.commit()
    conn.close()


@router.delete("/delete/{id_user}")
async def delete_user(id_user):
    """
    Supprime un utilisateur en fonction de son id (id_user)
    """

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    request = """
    DELETE FROM user 
    WHERE id = ?;
    """

    cursor.execute(request, (id_user,))
    conn.commit()
    conn.close()
