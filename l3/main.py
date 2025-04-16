import motor.motor_asyncio
from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from bson import ObjectId

# Підключення до MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.lab3

# FastAPI додаток
app = FastAPI(
    title="API для страхування життя та здоров'я",
    description="Цей API дозволяє керувати користувачами, страховими полісами та заявками.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")


# Pydantic моделі
class UserBase(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str

    class Config:
        from_attributes = True


class InsurancePolicyBase(BaseModel):
    policy_name: str
    coverage_amount: int


class InsurancePolicyCreate(InsurancePolicyBase):
    user_id: str


class InsurancePolicy(InsurancePolicyBase):
    id: str

    class Config:
        from_attributes = True


class ClaimBase(BaseModel):
    claim_amount: int


class ClaimCreate(ClaimBase):
    policy_id: str


class Claim(ClaimBase):
    id: str

    class Config:
        from_attributes = True

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/users/", response_model=User, summary="Створення нового користувача")
async def create_user(
        username: str = Form(...),
        role: str = Form(...)):
    existing_user = await db.users.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    user_data = {"username": username, "role": role}
    result = await db.users.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)

    return templates.TemplateResponse("success.html", {"request": {}, "user": user_data})


@app.get("/users/{user_id}", response_model=User, summary="Отримати інформацію про користувача",
         description="Цей ендпоінт дозволяє отримати інформацію про користувача за його ID.", tags=["Users"])
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return User(**user)

@app.put("/users/{user_id}", response_model=User, summary="Оновити інформацію про користувача",
         description="Цей ендпоінт дозволяє оновити інформацію користувача за його ID.", tags=["Users"])
async def update_user(user_id: str, user: UserCreate):
    existing_user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    updated_user["id"] = str(updated_user["_id"])
    del updated_user["_id"]
    return User(**updated_user)


@app.delete("/users/{user_id}", summary="Видалити користувача",
            description="Цей ендпоінт дозволяє видалити користувача за його ID.", tags=["Users"])
async def delete_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.delete_one({"_id": ObjectId(user_id)})

    return {"detail": "User deleted successfully"}


@app.post("/policies/", response_model=InsurancePolicy)
async def create_policy(
        policy_name: str = Form(...),
        coverage_amount: int = Form(...),
        user_id: str = Form(...)):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    policy_data = {"policy_name": policy_name, "coverage_amount": coverage_amount, "user_id": user_id}
    result = await db.policies.insert_one(policy_data)
    policy_data["_id"] = str(result.inserted_id)

    return templates.TemplateResponse("success_policies.html",
                                      {"request": {}, "policy": policy_data})


@app.get("/policies/{policy_id}", response_model=InsurancePolicy, summary="Отримати страховий поліс",
         description="Цей ендпоінт дозволяє отримати інформацію про страховий поліс за його ID.", tags=["Policies"])
async def get_policy(policy_id: str):
    policy = await db.policies.find_one({"_id": ObjectId(policy_id)})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    policy["id"] = str(policy["_id"])
    del policy["_id"]
    return InsurancePolicy(**policy)


@app.post("/claims/", response_model=Claim)
async def create_claim(
        claim_amount: int = Form(...),
        policy_id: str = Form(...)):
    policy = await db.policies.find_one({"_id": ObjectId(policy_id)})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    claim_data = {"claim_amount": claim_amount, "policy_id": policy_id}
    result = await db.claims.insert_one(claim_data)
    claim_data["_id"] = str(result.inserted_id)

    return templates.TemplateResponse("success_claims.html", {"request": {}, "claim": claim_data})


@app.get("/claims/{claim_id}", response_model=Claim, summary="Отримати заяву на страховий поліс",
         description="Цей ендпоінт дозволяє отримати інформацію про заяву за її ID.", tags=["Claims"])
async def get_claim(claim_id: str):
    claim = await db.claims.find_one({"_id": ObjectId(claim_id)})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    claim["id"] = str(claim["_id"])
    del claim["_id"]
    return Claim(**claim)

app.mount("/static", StaticFiles(directory="static"), name="static")
