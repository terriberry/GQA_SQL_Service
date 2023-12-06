from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from gqa_sql_service_package import chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, chain, path="\gqa-sql-service-chain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
