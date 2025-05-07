from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

# ✅ CORS setup — allows your HTML page to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files like index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# ✅ /tryon/ route to handle form POST
@app.post("/tryon/")
async def try_on(person: UploadFile = File(...), garment: UploadFile = File(...)):
    # Save uploaded images (optional for testing or processing)
    os.makedirs("uploads", exist_ok=True)
    person_path = f"uploads/person_{person.filename}"
    garment_path = f"uploads/garment_{garment.filename}"

    with open(person_path, "wb") as buffer:
        shutil.copyfileobj(person.file, buffer)
    with open(garment_path, "wb") as buffer:
        shutil.copyfileobj(garment.file, buffer)

    # 🧠 Replace this with your actual TryOn model logic
    # For now, just return a placeholder image (must exist)
    result_path = "static/sample_result.jpg"  # Put a test image in static/

    return FileResponse(result_path, media_type="image/jpeg")
