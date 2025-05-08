from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"message": "TryOn server is running."}

@app.post("/tryon/")
async def tryon(person: UploadFile = File(...), garment: UploadFile = File(...)):
    # Save uploaded files temporarily
    person_path = f"temp/{uuid.uuid4()}_{person.filename}"
    garment_path = f"temp/{uuid.uuid4()}_{garment.filename}"

    with open(person_path, "wb") as buffer:
        shutil.copyfileobj(person.file, buffer)
    with open(garment_path, "wb") as buffer:
        shutil.copyfileobj(garment.file, buffer)

    # === Replace this with real model inference ===
    # For now, copy a placeholder result image
    result_filename = f"{uuid.uuid4()}_result.jpg"
    result_path = f"static/{result_filename}"
    shutil.copy("sample_result.jpg", result_path)  # Replace with your real output

    # Clean up if needed (optional)
    os.remove(person_path)
    os.remove(garment_path)

    return JSONResponse(content={"image_url": f"/static/{result_filename}"})
