#!/usr/bin/env python3
"""Transcreve um vídeo/áudio em português com tempo por palavra (faster-whisper, modelo "small").
Uso: python3 transcrever.py video.mp4 [saida.words.json]
Saída: [{"w":"palavra","s":0.12,"e":0.70}, ...]  (segundos)
O modelo está dividido em partes < 100 MB (limite do GitHub); na 1ª execução elas são juntadas.
Instala o faster-whisper sozinho se faltar. O áudio é decodificado pelo ffmpeg.
"""
import json, os, sys, glob, subprocess, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__))
SHA = "3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671"
modelo = os.path.join(AQUI, "model.bin")
if not os.path.exists(modelo) or os.path.getsize(modelo) != 483546902:
    with open(modelo, "wb") as out:
        for p in sorted(glob.glob(os.path.join(AQUI, "model.bin.part_*"))):
            out.write(open(p, "rb").read())
    h = hashlib.sha256(open(modelo, "rb").read()).hexdigest()
    if h != SHA: sys.exit("model.bin corrompido (sha256 não confere)")
try:
    from faster_whisper import WhisperModel
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "faster-whisper"])
    from faster_whisper import WhisperModel
import numpy as np
video = sys.argv[1]
saida = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(video)[0] + ".words.json"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.float32)
m = WhisperModel(AQUI, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=True)
w = [{"w": x.word.strip(), "s": round(float(x.start), 2), "e": round(float(x.end), 2)}
     for s in segs for x in s.words if x.word.strip()]
json.dump(w, open(saida, "w"), ensure_ascii=False)
print("Pronto!", len(w), "palavras ->", saida)
