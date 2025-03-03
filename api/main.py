from fastapi import FastAPI
from routers import group

app = FastAPI()


app.include_router(group.router)