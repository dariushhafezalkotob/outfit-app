from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS so HTML from any origin can make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend URL for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST endpoint for /tryon
@app.post("/tryon/")
async def tryon(person: UploadFile = File(...), garment: UploadFile = File(...)):
    # For now, just return a static test image
    dummy_output_path = "static/sample_result.jpg"
    
    # Make sure the file exists
    if not os.path.exists(dummy_output_path):
        return {"error": "sample_result.jpg not found in static/"}

    return FileResponse(dummy_output_path, media_type="image/jpeg")

# Optional: health check
@app.get("/")
async def root():
    return {"message": "TryOn server is running."}
