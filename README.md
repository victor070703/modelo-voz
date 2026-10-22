# modelo-voz

Modelo de reconhecimento de voz **faster-whisper "small"** (licença MIT, original: [Systran/faster-whisper-small](https://huggingface.co/Systran/faster-whisper-small)), guardado aqui para a skill `skill-edicao-video` transcrever vídeos com tempo por palavra em ambientes onde o Hugging Face não é acessível.

O `model.bin` foi dividido em partes de 90 MB (limite de 100 MB do GitHub).

```bash
git clone --depth 1 https://github.com/victor070703/modelo-voz.git
python3 modelo-voz/transcrever.py video.mp4          # gera video.words.json
```
