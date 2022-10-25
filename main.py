from fastapi import FastAPI
from routers import route_auth
from schemas import SuccessMsg

app = FastAPI()
app.include_router(route_auth.router)


@app.get("/")
def read_root():
    return {"message": "welcome to"}
