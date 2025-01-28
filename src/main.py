from fastapi import FastAPI
from src.auth.views import user_router, auth_router

app = FastAPI(
    title="FastAPI JWT Authentication",
    description="A simple FastAPI app with JWT authentication",
    version="1.0.0",
)



app.include_router(auth_router)
app.include_router(user_router)
