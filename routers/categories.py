from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.list_categories(db, user.id)

@router.post("", status_code=201, response_model=schemas.CategoryOut)
def create_category(
    data: schemas.CategoryCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.create_category(db, user.id, data)
    if not category:
        raise HTTPException(status_code=409, detail="이미 같은 이름의 카테고리가 있습니다")
    return category

@router.patch("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    data: schemas.CategoryUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.get_my_category(db, user.id, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="해당하는 카테고리가 없습니다")

    updated = crud.update_category(db, category, data)
    if not updated:
        raise HTTPException(status_code=409, detail="이미 같은 이름의 카테고리가 있습니다")
    return updated

@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.get_my_category(db, user.id, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="해당하는 카테고리가 없습니다")

    count = crud.count_contacts_in_category(db, user.id, category_id)
    if count > 0:
        raise HTTPException(
            status_code=409,
            detail=f"이 카테고리를 사용하는 연락처가 {count}건 있어 삭제할 수 없습니다. 연락처의 종류를 먼저 변경하세요.",
        )

    crud.delete_category(db, category)
