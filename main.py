from fastapi import FastAPI
from github_helper import get_contributors, get_github_link
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


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
