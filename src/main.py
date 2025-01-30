from fastapi import FastAPI
from src.auth.views import user_router, auth_router
from src.profile.views import profile_route
from src.book.view import book_router
from src.reserve.view import reserve_router

app = FastAPI(
    title="FastAPI JWT Authentication",
    description="A simple FastAPI app with JWT authentication",
    version="1.0.0",
)



app.include_router(auth_router)
app.include_router(user_router)
app.include_router(profile_route)
app.include_router(book_router)
app.include_router(reserve_router)
