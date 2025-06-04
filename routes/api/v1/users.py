from fastapi import APIRouter, Depends, HTTPException, status
from services import UserService

user_router = APIRouter()
