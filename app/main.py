from fastapi import FastAPI, Depends, Body, File, UploadFile
from fastapi.responses import FileResponse

from typing import Union, Annotated

from contextlib import asynccontextmanager

from database import delete_tables, create_tables
from router import router as users_routers




# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("Base ready!")
#     await create_tables()    
#     print("Base ready!")
#     yield
#     print("off app")       


app=FastAPI()
app.include_router(users_routers)

@app.post("/")
async def add_file(uploaded_file:UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    headers = uploaded_file.headers
    print(filename)
    print(headers)
    with open(filename, "wb") as f:
        f.write(file.read())

@app.get("/{filename}")
async def get_file(filename:str):
    return FileResponse(filename)
