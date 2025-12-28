import torch
import numpy as np
import os
from chatterbox.tts import ChatterboxTTS
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from pydub import AudioSegment

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"=========================================")
print(f"MENGGUNAKAN DEVICE: {device.upper()}")
print(f"=========================================")

print("Memuat model Chatterbox-TTS-Indonesian...")
MODEL_REPO = "grandhigh/Chatterbox-TTS-Indonesian"
CHECKPOINT_FILENAME = "t3_cfg.safetensors"

model = ChatterboxTTS.from_pretrained(device=device)

# Unduh checkpoint dari Hugging Face Hub
checkpoint_path = hf_hub_download(repo_id=MODEL_REPO, filename=CHECKPOINT_FILENAME)
t3_state = load_file(checkpoint_path, device="cpu")

# Muat state_dict ke dalam model
model.t3.load_state_dict(t3_state)
torch.cuda.empty_cache()
print("Model SIAP. Siap menerima input.")
print("-" * 40)

def generate_speech_with_accent(text_to_speak, accent_audio_path, output_filename):
    """
    Fungsi untuk generate audio dengan kloning aksen dan menyimpannya ke file.
    """
    
    # Buat folder output jika belum ada
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output_filename)
    
    # Cek apakah file referensi ada
    if not os.path.exists(accent_audio_path):
        print(f"!! ERROR: File referensi tidak ditemukan di: {accent_audio_path}")
        return

    print(f"Memulai kloning suara untuk: '{text_to_speak[:30]}...'")
    print(f"Menggunakan aksen dari: {accent_audio_path}")

    # Hasilkan audio
    wav_audio_clone = model.generate(
        text_to_speak,
        audio_prompt_path=accent_audio_path
    )
    
    try:
        # Ambil data mentah 
        audio_data_float = wav_audio_clone.numpy()
        
        # Konversi ke int16 
        audio_data_int16 = (audio_data_float * 32767).astype(np.int16)
        
        # Buat "Audio Segment" 
        audio_segment = AudioSegment(
            data=audio_data_int16.tobytes(), 
            sample_width=audio_data_int16.dtype.itemsize, 
            frame_rate=model.sr, 
            channels=1 
        )
        
        # Ekspor sebagai file .wav 
        audio_segment.export(output_path, format="wav")
        
        print(f"SUKSES! Audio disimpan di: {output_path}")
        
    except Exception as e:
        print(f"!! ERROR SAAT MENYIMPAN FILE (pydub): {e}")
        print("Pastikan 'ffmpeg' terinstal. Coba jalankan 'pip install ffmpeg-python'")
        
    print("-" * 40)

if __name__ == "__main__":
    
    REFERENSI_JAWA = os.path.join("audio_referensi", "aksen_sunda_priav2.wav")
    REFERENSI_SUNDA = os.path.join("audio_referensi", "aksen_sunda_wanita.wav")
    
    generate_speech_with_accent(
        text_to_speak="Tah, ieu abdi, Gemini. Abdi nuju nyobian nyarios ku basa Sunda. Kumaha, ceuk Akang/Teteh, atos sae? Mugi-mugi pas nya kangge text to speech na. Hoyong naon deui?",
        accent_audio_path=REFERENSI_JAWA,
        output_filename="hasil_sunda_02.wav"
    )
    