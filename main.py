from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class ImagePostRequest(BaseModel):
   keyword: str
   Requirements: str

class ImageResponse(BaseModel):
    image_url: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/generate/image", response_model=ImageResponse)
async def generateImage(request: ImagePostRequest):
    response = client.images.generate(
          model="dall-e-3",
          prompt=f'{request.keyword} ${request.Requirements}',
          quality="standard",
          size="1024x1024",
          n=1,
      )
    image_url = response.data[0].url
    return ImageResponse(image_url=image_url)
