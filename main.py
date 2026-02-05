
from fastapi import FastAPI
from contextlib import asynccontextmanager
from enum import Enum
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer


models = {}


@asynccontextmanager 
async def lifespan(app: FastAPI):
    models["model"] = AutoModelForSeq2SeqLM.from_pretrained("bigscience/mt0-small")
    checkpoint = "bigscience/mt0-small"
    models["tokenizer"] = AutoTokenizer.from_pretrained(checkpoint)
    yield
    models.clear()
    
    
 
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI(lifespan=lifespan)



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





@app.get("/translate/{text}")
async def translate_text(text: str):
    inputs = models["tokenizer"](text, return_tensors="pt")
    outputs = models["model"].generate(**inputs)
    decoded_output = models["tokenizer"].decode(outputs[0], skip_special_tokens=True)
    return {"translation": decoded_output}


