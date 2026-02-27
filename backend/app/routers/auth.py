from fastapi import APIRouter
from pydantic import BaseModel

from app.store import user

router = APIRouter()


class LoginRequest(BaseModel):
    phone: str
    password: str


@router.post("/login")
def login(req: LoginRequest):
    if not req.phone or not req.password:
        return {"success": False, "message": "请填写手机号和密码"}
    return {"success": True, "user": user}


@router.get("/user")
def get_user():
    return user


@router.post("/logout")
def logout():
    return {"success": True}
