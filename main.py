# -*- coding:utf-8 -*-

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deps import get_token
from services.suno import suno_service

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(token: str = Depends(get_token)):
    return await suno_service.generate_music(token)
