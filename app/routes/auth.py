from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Token, AuthData
from app.core.security import get_password_hash, verify_password
from app.core.jwt_handler import create_access_token
from pydantic import BaseModel
import sqlite3 

router = APIRouter()

@router.post("/register")
def register(create_user: UserCreate):

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    pseudo = create_user.pseudo
    email = create_user.email
    password = create_user.password
    is_coach = create_user.is_coach

    request = """
    SELECT id, pseudo, email, password, is_coach 
    FROM user
    WHERE email = ?
    """

    cursor.execute(request, (email,))
    existing_user = cursor.fetchall()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email utilisateur déjà utilisé")
    
    hashed_password = get_password_hash(password)

    request_2 = """
    INSERT INTO user (pseudo, email, password, is_coach)
    VALUES (?, ?, ?, ?);"""

    cursor.execute(request_2, (pseudo, email, hashed_password, is_coach))
    conn.commit()
    conn.close()


@router.post("/login")
def login(form:AuthData):
    # statement = select(User).where(User.username == form.username)

    conn = sqlite3.connect('database.db') # Connexion à la base de données
    cursor = conn.cursor() # Création d'un curseur

    email = str(form.email)

    print(f"debug email :{email}")

    request = """
    SELECT id, pseudo, email, password, is_coach FROM user
    WHERE email = ?;
    """

    cursor.execute(request, (email,))
    db_user = cursor.fetchone()
    print(db_user)

    if not db_user or not verify_password(form.password, db_user[3]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user[2], "id": db_user[0], "is_coach": db_user[4]})
    return {"access_token": access_token, "token_type": "bearer"}