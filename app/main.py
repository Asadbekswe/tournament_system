from fastapi import FastAPI
import logging

from app.api.tournament import router

app = FastAPI(title='Tournament API')

app.include_router(router)



logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)