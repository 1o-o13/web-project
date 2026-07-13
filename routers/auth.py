from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models, schemas, crud, security
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

def get_current_user(session_id: str | None = Cookie(default=None), db: Session = Depends(get_db)) -> models.User:
    if session_id is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    user = crud.get_session_user(db, session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    return user

@router.post("/signup", status_code=201, response_model=schemas.UserOut)
def signup(data: schemas.SignupIn, db: Session = Depends(get_db)):
    user = crud.create_user(db, data)
    if user is None:
        raise HTTPException(status_code=409, detail="이미 있는 아이디입니다")
    return user

@router.post("/login", response_model=dict)
def login(data: schemas.SignupIn, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, data.username)
    if user is None or not security.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다")

    session_id = crud.create_login_session(db, user.id)
    response = JSONResponse(content={"message": "로그인 성공"}, status_code=200)
    response.set_cookie("session_id", session_id, httponly=True, path="/")
    return response

@router.post("/logout", response_model=dict)
def logout(session_id: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    if session_id:
        crud.delete_login_session(db, session_id)

    response = JSONResponse(content={"message": "로그아웃 되었습니다"}, status_code=200)
    response.delete_cookie("session_id", path="/")
    return response

@router.get("/me", response_model=schemas.UserOut)
def get_me(user: models.User = Depends(get_current_user)):
    return user
