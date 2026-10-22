# modelo-voz

Somente **dados**: modelo de reconhecimento de voz faster-whisper "small" (licença MIT, original: Systran/faster-whisper-small), usado pela skill `skill-edicao-video`. O código de transcrição fica na própria skill.

O `model.bin` foi dividido em partes de 90 MB (limite do GitHub). Para juntar: `cat model.bin.part_* > model.bin`
(sha256: 3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671).
