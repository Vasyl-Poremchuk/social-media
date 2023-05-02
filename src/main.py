from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.routers import auth, comment, like, post, user
from src.config import settings

app = FastAPI(title="SocialMedia")

app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(router=auth.router)
app.include_router(router=comment.router)
app.include_router(router=like.router)
app.include_router(router=post.router)
app.include_router(router=user.router)


@app.get("/", tags=["Root Endpoint"])
def root() -> dict[str, str]:
    """
    A function is the root endpoint of an application.
    """
    return {"message": "Hi, there!"}
