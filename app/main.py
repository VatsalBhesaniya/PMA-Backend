from fastapi import FastAPI
from . import models
from .database import engine
from .routers import task, user, auth, project, note, document, member
from fastapi.middleware.cors import CORSMiddleware

# if we use sqlalchemy without alembic then to generate tables we need below line
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(member.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(note.router)
app.include_router(document.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
