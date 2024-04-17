import uvicorn
from fastapi import FastAPI, Depends, HTTPException
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from routes import router

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
