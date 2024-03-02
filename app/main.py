# FastApi main.py

from fastapi import FastAPI
from routes.routers import router

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json",
    description="Description text", version='1.0.0', summary="Summery Text"
)

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='debug')
