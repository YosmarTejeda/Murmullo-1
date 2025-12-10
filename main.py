from fastapi import FastAPI, HTTPException
from pydub import AudioSegment
import base64
import io
import numpy as np

app = FastAPI()

@app.post("/process_audio/")
async def process_audio(data: dict):
    try:
        audio_base64 = data["audio_base64"]

        # Decodificar
        decoded_audio = base64.b64decode(audio_base64)
        audio = AudioSegment.from_file(io.BytesIO(decoded_audio), format="aac")

        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # RMS y decibelios
        rms = np.sqrt(np.mean(samples ** 2))
        if rms == 0:
            db = -float('inf')
        else:
            db = 20 * np.log10(rms)

        # Máximo
        peak = np.max(np.abs(samples))
        if peak == 0:
            db_peak = -float('inf')
        else:
            db_peak = 20 * np.log10(peak)

        return {
            "average_db": float(round(db, 2)),
            "peak_db": float(round(db_peak, 2)),
            "duration_sec": float(round(len(audio) / 1000, 2))
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
