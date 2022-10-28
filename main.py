from fastapi import FastAPI
from schemas import models as UsageModel

app = FastAPI()


@app.get("/")
async def index():
    return {"api": "fastapi"}


@app.post("/simple-users/", response_model=UsageModel.SimpleUser)
async def read_simple_user(user: UsageModel.SimpleUser):
    return user


@app.post("/recursive-models/", response_model=UsageModel.Spam)
async def read_spam_data(spam: UsageModel.Spam):
    return spam
