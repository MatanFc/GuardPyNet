from fastapi import FastAPI
from github_helper import get_contributors
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from db.config import engine, Base, get_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return "hello world"


@app.get("/contributors/{package_name}")
async def get_package_contributors(package_name: str):
    contributors = get_contributors(package_name)
    return {
        "package": package_name,
        "contributors": contributors,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
