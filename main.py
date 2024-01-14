from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "hello world"


@app.get("/contributors/{package_name}")
def get_contributors(package_name: str):
    return {
        "package": package_name,
        "contributors": ["dummy contributor1", "dummy contributor2"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
