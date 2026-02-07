
from fastapi import FastAPI
from contextlib import asynccontextmanager
from enum import Enum
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