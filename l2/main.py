from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles



# Створюємо Pydantic моделі для User, Policy, Claim
class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # замінено orm_mode на from_attributes


class InsurancePolicyBase(BaseModel):
    policy_name: str
    coverage_amount: int


class InsurancePolicyCreate(InsurancePolicyBase):
    user_id: int


class InsurancePolicy(InsurancePolicyBase):
    id: int

    class Config:
        from_attributes = True  # замінено orm_mode на from_attributes


class ClaimBase(BaseModel):
    claim_amount: int


class ClaimCreate(ClaimBase):
    policy_id: int


class Claim(ClaimBase):
    id: int

    class Config:
        from_attributes = True  # замінено orm_mode на from_attributes


app = FastAPI(
    title="API для страхування життя та здоров'я",
    description="Цей API дозволяє керувати користувачами, страховими полісами та заявками.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/users/", response_model=User, summary="Створення нового користувача",
          description="Цей ендпоінт дозволяє створити нового користувача.", tags=["Users"])
def create_user(username: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    user = models.User(username=username, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Після успішного створення перенаправляємо на сторінку успіху
    return RedirectResponse(url=f"/success/{user.id}", status_code=303)

@app.get("/success/{user_id}", response_class=HTMLResponse)
def success_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Виводимо ID користувача на сторінці
    return templates.TemplateResponse("success.html", {"request": request, "user": user, "user_id": user.id})
@app.get("/users/{user_id}", response_model=User, summary="Отримати інформацію про користувача",
         description="Цей ендпоінт дозволяє отримати інформацію про користувача за його ID.", tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User, summary="Оновити інформацію про користувача",
         description="Цей ендпоінт дозволяє оновити інформацію користувача за його ID.", tags=["Users"])
def update_user(user_id: int, username: str = None, role: str = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user.username = username
    if role:
        user.role = role

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}", summary="Видалити користувача",
            description="Цей ендпоінт дозволяє видалити користувача за його ID.", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"detail": "User deleted successfully"}


@app.post("/policies/", response_model=InsurancePolicy, summary="Створити страховий поліс",
          description="Цей ендпоінт дозволяє створити страховий поліс для користувача.", tags=["Policies"])
def create_policy(policy_name: str = Form(...), coverage_amount: int = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    # Перевіряємо, чи існує користувач
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Створюємо новий поліс
    policy = models.InsurancePolicy(policy_name=policy_name, coverage_amount=coverage_amount, user_id=user_id)
    db.add(policy)
    db.commit()
    db.refresh(policy)

    return RedirectResponse(url=f"/success_policies/{policy.id}", status_code=303)

@app.get("/policies/{policy_id}", response_model=InsurancePolicy, summary="Отримати страховий поліс",
         description="Цей ендпоінт дозволяє отримати інформацію про страховий поліс за його ID.", tags=["Policies"])
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(models.InsurancePolicy).filter(models.InsurancePolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@app.post("/claims/", response_model=Claim, summary="Створити заяву на страховий поліс",
          description="Цей ендпоінт дозволяє створити заяву на страховий поліс.", tags=["Claims"])
def create_claim(claim_amount: int = Form(...), policy_id: int = Form(...), db: Session = Depends(get_db)):
    policy = db.query(models.InsurancePolicy).filter(models.InsurancePolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    claim = models.Claim(policy_id=policy_id, claim_amount=claim_amount)
    db.add(claim)
    db.commit()
    db.refresh(claim)

    return RedirectResponse(url=f"/success_claims/{claim.id}", status_code=303)


@app.get("/claims/{claim_id}", response_model=Claim, summary="Отримати заяву на страховий поліс",
         description="Цей ендпоінт дозволяє отримати інформацію про заяву за її ID.", tags=["Claims"])
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/success_claims/{claim_id}", response_class=HTMLResponse)
def success_claim(request: Request, claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return templates.TemplateResponse("success_claims.html", {"request": request, "claim": claim, "claim_id": claim.id})

@app.get("/success_policies/{policy_id}", response_class=HTMLResponse)
def success_policy(request: Request, policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(models.InsurancePolicy).filter(models.InsurancePolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return templates.TemplateResponse("success_policies.html", {"request": request, "policy": policy, "policy_id": policy.id})

