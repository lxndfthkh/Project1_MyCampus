from fastapi import FastAPI
from mycampus.routers.folders_router import router as folders_router
from mycampus.routers.files_router import router as files_router


app = FastAPI()
app.include_router(folders_router)
app.include_router(files_router)


@app.get("/")
def read_root():
    return{"message": "Hello, MyCampus!"}