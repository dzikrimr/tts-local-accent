import torch
import numpy as np
import os
import uvicorn
import io  
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from chatterbox.tts import ChatterboxTTS
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AksaTTSBackend")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"=========================================")
print(f"MENGGUNAKAN DEVICE: {device.upper()}")
print(f"=========================================")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENSI_DIR = os.path.join(BASE_DIR, "audio_referensi")
os.makedirs(REFERENSI_DIR, exist_ok=True) 

print("Memuat model Chatterbox-TTS-Indonesian (Cold Start)...")
try:
    MODEL_REPO = "grandhigh/Chatterbox-TTS-Indonesian"
    CHECKPOINT_FILENAME = "t3_cfg.safetensors"
    
    model = ChatterboxTTS.from_pretrained(device=device)
    
    checkpoint_path = hf_hub_download(repo_id=MODEL_REPO, filename=CHECKPOINT_FILENAME)
    t3_state = load_file(checkpoint_path, device="cpu")
    
    model.t3.load_state_dict(t3_state)
    torch.cuda.empty_cache()
    print("=========================================")
    print("MODEL SIAP (WARM). Server siap menerima request.")
    print("=========================================")

except Exception as e:
    print(f"FATAL ERROR: Gagal memuat model. {e}")
    model = None

ACCENT_LIBRARY = {
    "aceh": "aksen_aceh_pria.wav",
    "bali": "aksen_bali_pria.wav",
    "banjar": "aksen_banjar_wanita.wav",
    "batak": "aksen_batak_pria.wav",
    "betawi": "aksen_betawi_pria.wav",
    "jawa": "aksen_jawa_pria.wav",
    "maluku": "aksen_maluku_pria.wav",
    "melayu": "aksen_melayu_pria.wav",
    "minang": "aksen_minang_pria.wav",
    "ntt": "aksen_ntt_pria.wav",
    "papua": "aksen_papua_pria.wav",
    "pontianak": "aksen_pontianak_wanita.wav",
    "sulsel": "aksen_sulsel_pria.wav",
    "sulut": "aksen_sulut_pria.wav",
    "sunda": "aksen_sunda_pria.wav",
    "sunda_v2": "aksen_sunda_pria.wav",
    "default": "aksen_default_pria.wav"
}


class TTSRequest(BaseModel):
    text: str
    accent_id: str 

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Aksa TTS Backend")

# Fungsi Generator
async def audio_stream_generator(text_to_speak: str, accent_audio_path: str):
    """
    Menghasilkan audio utuh di memori, lalu mengirimkannya 
    secara streaming (potongan demi potongan) ke klien.
    Ini memecahkan masalah "menunggu download file utuh".
    """
    logger.info("Memulai sintesis (Generate)...")
    
    # Generate Audio
    wav_audio_clone = model.generate(
        text_to_speak,
        audio_prompt_path=accent_audio_path
    )
    
    logger.info("Sintesis selesai. Mengonversi ke WAV di memori...")
    
    # Konversi ke format WAV
    audio_data_float = wav_audio_clone.numpy()
    audio_data_int16 = (audio_data_float * 32767).astype(np.int16)
    
    audio_segment = AudioSegment(
        data=audio_data_int16.tobytes(),
        sample_width=audio_data_int16.dtype.itemsize,
        frame_rate=model.sr,
        channels=1
    )
    
    file_in_memory = io.BytesIO()
    audio_segment.export(file_in_memory, format="wav")
    file_in_memory.seek(0) # Kembali ke awal "file"
    
    logger.info("Memulai streaming audio ke klien...")
    
    # Kirim "file virtual"
    chunk_size = 1024 * 1024
    while True:
        chunk = file_in_memory.read(chunk_size)
        if not chunk:
            break # Selesai
        yield chunk
        await asyncio.sleep(0.01)
    
    logger.info("Streaming audio selesai.")


@app.get("/")
def read_root():
    return {"status": "Aksa TTS Backend is running."}

@app.post("/stream-speech/")
async def stream_speech_endpoint(request: TTSRequest):
    """
    Menerima Teks dan ID Aksen, lalu MENGEMBALIKAN STREAMING AUDIO
    yang bisa langsung diputar oleh Jetpack Compose.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model TTS tidak siap (Service Unavailable).")

    logger.info(f"Menerima request streaming untuk aksen: {request.accent_id}")
    
    accent_filename = ACCENT_LIBRARY.get(request.accent_id.lower(), ACCENT_LIBRARY["default"])
    accent_audio_path = os.path.join(REFERENSI_DIR, accent_filename)
    
    if not os.path.exists(accent_audio_path):
        logger.error(f"File referensi tidak ditemukan: {accent_audio_path}")
        raise HTTPException(status_code=404, detail=f"File referensi untuk aksen '{request.accent_id}' tidak ditemukan di server.")

    audio_generator = audio_stream_generator(request.text, accent_audio_path)
    
    return StreamingResponse(audio_generator, media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)