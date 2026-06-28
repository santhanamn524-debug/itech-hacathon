from fastapi import APIRouter
from tools.get_schema import get_schema

router = APIRouter()

@router.get("/schema")
def get_db_schema():
    return get_schema()