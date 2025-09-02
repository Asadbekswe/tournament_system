from fastapi import FastAPI

app = FastAPI()


@app.post('/tournaments')
async def create_tournaments():
    return {'message': "Hello World !!!"}
