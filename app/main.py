from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import sqlite3
from app.core.jwt_handler import get_current_user
from app.routes import user, test, caracteristic, test_type, auth

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["user"])
app.include_router(auth.router, prefix="", tags=["authentication"])
app.include_router(caracteristic.router, prefix="/caracteristics", tags=["caracteristic"])
app.include_router(test.router, prefix="/tests", tags=["test"])
app.include_router(test_type.router, prefix="/test_types", tags=["test_type"])
