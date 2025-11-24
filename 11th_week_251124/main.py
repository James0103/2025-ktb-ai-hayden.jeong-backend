from fastapi import FastAPI
import uvicorn
from router.db_router import db_router
from router.misc_router import misc_router

app = FastAPI()

app.include_router(db_router)
app.include_router(misc_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
