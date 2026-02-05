
from fastapi import FastAPI

app = FastAPI()


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
async def get_student_id(student_id):
    for students in fake_DB.get("students"):
        if students.get("id") == int(student_id) :
            return {"name":students.get("name")}
            
        
    return {"error": "student name not exist"}
            