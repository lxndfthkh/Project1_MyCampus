from fastapi import FastAPI
from .routers.folders_router import router as folders_router


app = FastAPI()
app.include_router(folders_router)

@app.get("/")
def read_root():
    return{"message": "Hello, MyCampus!"}