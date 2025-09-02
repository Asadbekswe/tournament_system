from fastapi import FastAPI
import logging

from app.api.tournament import router

app = FastAPI(title='Tournament API')

app.include_router(router)



logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
