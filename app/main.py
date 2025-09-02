from fastapi import FastAPI

from app.api.tournament import router

app = FastAPI(title='Tournament API')

app.include_router(router)
