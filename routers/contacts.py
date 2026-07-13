from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("", response_model=schemas.ContactListOut)
def list_contacts(
    name: str | None = Query(None),
    category_id: int | None = Query(None),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contacts = crud.list_contacts(db, user.id, name=name, category_id=category_id)
    items = [
        schemas.ContactOut(
            id=c.id,
            name=c.name,
            phone=c.phone,
            addr=c.addr,
            category_id=c.category_id,
            category_name=c.category.name,
        )
        for c in contacts
    ]
    return schemas.ContactListOut(total=len(items), items=items)

@router.post("", status_code=201, response_model=schemas.ContactOut)
def create_contact(
    data: schemas.ContactCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.get_my_category(db, user.id, data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")

    contact = crud.create_contact(db, user.id, data)
    if not contact:
        raise HTTPException(status_code=409, detail="이미 등록된 전화번호입니다")

    return schemas.ContactOut(
        id=contact.id,
        name=contact.name,
        phone=contact.phone,
        addr=contact.addr,
        category_id=contact.category_id,
        category_name=category.name,
    )

@router.patch("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(
    contact_id: int,
    data: schemas.ContactUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = crud.get_my_contact(db, user.id, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="해당하는 회원 정보가 없습니다")

    if data.category_id:
        category = crud.get_my_category(db, user.id, data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")
    else:
        category = contact.category

    updated = crud.update_contact(db, contact, data)
    if not updated:
        raise HTTPException(status_code=409, detail="이미 등록된 전화번호입니다")

    return schemas.ContactOut(
        id=updated.id,
        name=updated.name,
        phone=updated.phone,
        addr=updated.addr,
        category_id=updated.category_id,
        category_name=category.name,
    )

@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = crud.get_my_contact(db, user.id, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="해당하는 회원 정보가 없습니다")

    crud.delete_contact(db, contact)
