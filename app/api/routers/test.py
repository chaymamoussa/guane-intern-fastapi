from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, crud
from app.api import deps
from app.crud import superuser_crud


router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}