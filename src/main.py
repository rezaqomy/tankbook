from fastapi import FastAPI
from src.auth.views import user_router, auth_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
