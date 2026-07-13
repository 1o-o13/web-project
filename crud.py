from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas, security

# ===== 인증 CRUD =====
def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, signup_data: schemas.SignupIn) -> models.User | None:
    existing = get_user_by_username(db, signup_data.username)
    if existing:
        return None

    hashed = security.hash_password(signup_data.password)
    user = models.User(username=signup_data.username, password_hash=hashed)
    db.add(user)
    db.flush()

    default_categories = [
        models.Category(user_id=user.id, name="가족"),
        models.Category(user_id=user.id, name="친구"),
        models.Category(user_id=user.id, name="기타"),
    ]
    db.add_all(default_categories)
    db.commit()
    db.refresh(user)
    return user

def create_login_session(db: Session, user_id: int) -> str:
    import secrets
    session_id = secrets.token_hex(32)
    session = models.LoginSession(session_id=session_id, user_id=user_id)
    db.add(session)
    db.commit()
    return session_id

def get_session_user(db: Session, session_id: str) -> models.User | None:
    session = db.query(models.LoginSession).filter(models.LoginSession.session_id == session_id).first()
    if not session:
        return None
    return session.user

def delete_login_session(db: Session, session_id: str) -> None:
    db.query(models.LoginSession).filter(models.LoginSession.session_id == session_id).delete()
    db.commit()

# ===== 연락처 CRUD =====
def list_contacts(db: Session, user_id: int, name: str | None = None, category_id: int | None = None) -> list[models.Contact]:
    query = db.query(models.Contact).filter(models.Contact.user_id == user_id)
    if name:
        query = query.filter(models.Contact.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(models.Contact.category_id == category_id)
    return query.all()

def get_my_contact(db: Session, user_id: int, contact_id: int) -> models.Contact | None:
    return db.query(models.Contact).filter(
        and_(models.Contact.id == contact_id, models.Contact.user_id == user_id)
    ).first()

def create_contact(db: Session, user_id: int, data: schemas.ContactCreate) -> models.Contact | None:
    existing = db.query(models.Contact).filter(
        and_(models.Contact.user_id == user_id, models.Contact.phone == data.phone)
    ).first()
    if existing:
        return None

    contact = models.Contact(
        user_id=user_id,
        category_id=data.category_id,
        name=data.name,
        phone=data.phone,
        addr=data.addr,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def update_contact(db: Session, contact: models.Contact, data: schemas.ContactUpdate) -> models.Contact | None:
    update_data = data.model_dump(exclude_unset=True)

    if "phone" in update_data and data.phone != contact.phone:
        existing = db.query(models.Contact).filter(
            and_(
                models.Contact.user_id == contact.user_id,
                models.Contact.phone == data.phone,
                models.Contact.id != contact.id,
            )
        ).first()
        if existing:
            return None

    for field, value in update_data.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact

def delete_contact(db: Session, contact: models.Contact) -> None:
    db.delete(contact)
    db.commit()

# ===== 카테고리 CRUD =====
def list_categories(db: Session, user_id: int) -> list[models.Category]:
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()

def get_my_category(db: Session, user_id: int, category_id: int) -> models.Category | None:
    return db.query(models.Category).filter(
        and_(models.Category.id == category_id, models.Category.user_id == user_id)
    ).first()

def create_category(db: Session, user_id: int, data: schemas.CategoryCreate) -> models.Category | None:
    existing = db.query(models.Category).filter(
        and_(models.Category.user_id == user_id, models.Category.name == data.name)
    ).first()
    if existing:
        return None

    category = models.Category(user_id=user_id, name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category: models.Category, data: schemas.CategoryUpdate) -> models.Category | None:
    existing = db.query(models.Category).filter(
        and_(
            models.Category.user_id == category.user_id,
            models.Category.name == data.name,
            models.Category.id != category.id,
        )
    ).first()
    if existing:
        return None

    category.name = data.name
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category: models.Category) -> None:
    db.delete(category)
    db.commit()

def count_contacts_in_category(db: Session, user_id: int, category_id: int) -> int:
    return db.query(models.Contact).filter(
        and_(models.Contact.user_id == user_id, models.Contact.category_id == category_id)
    ).count()
