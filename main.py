from fastapi import FastAPI, Request
from routers import route_auth
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import SuccessMsg, CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

app = FastAPI()
app.include_router(route_auth.router)

origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':  exc.message
                 }
    )


@app.get("/")
def read_root():
    return {"message": "welcome to"}
