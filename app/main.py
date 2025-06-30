from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


import uvicorn


DB_URL = "sqlite+aiosqlite:///mydb.db"

engine = create_async_engine(DB_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI()

@app.get("/home")
async def home():
    return {"Helo it is Home page"}


if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
