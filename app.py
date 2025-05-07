from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from gradio_client import Client, file
import shutil
import uuid
import os

app = FastAPI()
client = Client("frogleo/AI-Clothes-Changer")

@app.post("/tryon/")
async def tryon(person: UploadFile = File(...), garment: UploadFile = File(...)):
    # Save files locally
    person_path = f"temp/{uuid.uuid4()}_{person.filename}"
    garment_path = f"temp/{uuid.uuid4()}_{garment.filename}"

    with open(person_path, "wb") as f:
        shutil.copyfileobj(person.file, f)
    with open(garment_path, "wb") as f:
        shutil.copyfileobj(garment.file, f)

    # Call HuggingFace API
    result_path = client.predict(
        person=file(person_path),
        garment=file(garment_path),
        denoise_steps=30,
        seed=42,
        api_name="/infer"
    )

    return FileResponse(result_path, media_type="image/jpeg")

