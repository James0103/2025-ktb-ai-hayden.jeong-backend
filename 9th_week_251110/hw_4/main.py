from fastapi import FastAPI
import uvicorn
from router.user_router import user_router
from router.post_router import post_router
from router.reply_router import reply_router
from router.misc_router import misc_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(reply_router)
app.include_router(misc_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)