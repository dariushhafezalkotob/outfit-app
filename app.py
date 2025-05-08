from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from gradio_client import Client, file
import shutil
import os

app = FastAPI()

# CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TryOn server is running."}

@app.post("/tryon/")
async def tryon(person: UploadFile = File(...), garment: UploadFile = File(...)):
    # Save uploaded files temporarily
    with open("person.jpg", "wb") as buffer:
        shutil.copyfileobj(person.file, buffer)
    with open("garment.jpg", "wb") as buffer:
        shutil.copyfileobj(garment.file, buffer)

    # Call Hugging Face API
    client = Client("frogleo/AI-Clothes-Changer")
    result = client.predict(
        person=file("person.jpg"),
        garment=file("garment.jpg"),
        denoise_steps=30,
        seed=42,
        api_name="/infer"
    )

    # Save result
    result_path = "static/output.jpg"
    os.makedirs("static", exist_ok=True)
    shutil.copy(result, result_path)

    return {"image_url": f"/static/output.jpg"}
