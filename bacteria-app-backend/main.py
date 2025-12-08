from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from processing_bridge import pipeline_completo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

def salvar_upload(file_obj):
    path = os.path.join(TEMP_DIR, file_obj.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file_obj.file, buffer)
    return path

@app.post("/api/analyze")
async def analyze_full(
    # Amostra
    sample_raw: UploadFile = File(...),
    sample_hdr: UploadFile = File(...),
    # Dark
    dark_raw: UploadFile = File(...),
    dark_hdr: UploadFile = File(...),
    # White
    white_raw: UploadFile = File(...),
    white_hdr: UploadFile = File(...),
    # Opções
    snv: str = Form("false"),
    savgol: str = Form("false")
):
    try:
        # 1. Salva tudo
        paths = {
            'sample_raw': salvar_upload(sample_raw),
            'sample_hdr': salvar_upload(sample_hdr),
            'dark_raw': salvar_upload(dark_raw),
            'dark_hdr': salvar_upload(dark_hdr),
            'white_raw': salvar_upload(white_raw),
            'white_hdr': salvar_upload(white_hdr),
        }

        # 2. Converte opções
        options = {
            'snv': snv.lower() == 'true',
            'savgol': savgol.lower() == 'true'
        }

        # 3. Roda pipeline
        resultados = pipeline_completo(paths, options)
        
        return {"status": "success", "data": resultados}

    except Exception as e:
        print(f"Erro: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)