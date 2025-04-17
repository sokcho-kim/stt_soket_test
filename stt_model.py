# stt_model.py

import whisper

# 모델 로드 (초기에 한 번만)
model = whisper.load_model("base")  # "tiny", "small", "medium" 도 가능

def transcribe_audio(audio_path: str) -> str:
    """
    입력된 오디오 파일 경로를 Whisper로 텍스트로 변환한다.
    """
    try:
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"[ERROR] Whisper STT 실패: {e}")
        return "[인식 실패]"
