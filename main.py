# main.py

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from stt_model import transcribe_audio
from utils import save_audio_temp

app = FastAPI()

# CORS 허용 (테스트용 전체 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()
    print("🟢 클라이언트 연결")

    try:
        while True:
            # 1. 음성 데이터 수신
            audio_bytes = await websocket.receive_bytes()
            print(f"📥 받은 음성 바이트: {len(audio_bytes)} bytes")

            # 🔍 디버깅: 수신한 오디오 원본 그대로 저장해보기
            import uuid
            debug_path = f"debug_{uuid.uuid4().hex}.wav"
            with open(debug_path, "wb") as f:
                f.write(audio_bytes)
            print(f"📁 디버그용 원본 저장 완료: {debug_path}")

            # 2. 임시 wav 파일로 저장
            wav_path = save_audio_temp(audio_bytes)

            # 3. Whisper로 텍스트 변환
            text = transcribe_audio(wav_path)
            print(f"🧠 STT 결과: {text}")

            # 4. 텍스트 응답 전송
            await websocket.send_text(text)

    except Exception as e:
        print("❌ 연결 종료:", e)
        await websocket.close()
