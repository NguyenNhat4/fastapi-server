
from fastapi import FastAPI
from contextlib import asynccontextmanager
from enum import Enum
from huggingface_hub import User
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from pydantic import BaseModel
models = {}


@asynccontextmanager 
async def lifespan(app: FastAPI):
    models["model"] = AutoModelForSeq2SeqLM.from_pretrained("bigscience/mt0-small")
    checkpoint = "bigscience/mt0-small"
    models["tokenizer"] = AutoTokenizer.from_pretrained(checkpoint)
    yield
    
    
 
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI(lifespan=lifespan)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

fake_DB = {
    "students": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},   
    {"id": 3, "name": "Charlie"},
    ]
    
}



@app.get("/")
async def root():
    return {"message": "Hello World 123"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


@app.get("/get_student/{student_id}")
async def get_student_id(student_id: int):
    for students in fake_DB.get("students"):
        if students.get("id") == student_id:
            return {"name":students.get("name")}
            
    return {"error": "student name not exist"}
            

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

class Language(str, Enum):
    french = "fr"
    vietnam = "vi"
    english = "en"
class TranslationRequest(BaseModel):
    text: str
    language: Language


@app.post("/translate/")
async def translate_text(res: TranslationRequest):

    if res.language == Language.french:
        text = "Translate  to French: " + res.text
    elif res.language == Language.vietnam:
        text = "translate to Vietnamese: " + res.text
    else:
        text = "translate to English: " + res.text    
    
    inputs = models["tokenizer"](text, return_tensors="pt")
    outputs = models["model"].generate(**inputs)
    decoded_output = models["tokenizer"].decode(outputs[0], skip_special_tokens=True)
    return {"translation": decoded_output}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item



from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from pydantic import BaseModel
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
def fake_hash_password(password: str):
    return "fakehashed" + password
    
    

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    print("token:", token)
    
    return user



@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print("current_user:", current_user.full_name)
    return current_user


