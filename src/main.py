from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, comment, like, post, user

app = FastAPI(title="SocialMedia")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
