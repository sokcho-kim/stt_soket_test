import websocket
import wave
import time

# 서버 주소 (포트 맞춰줘)
WS_URL = "ws://localhost:8018/ws/audio"

# 너의 테스트 wav 파일
# C:\ai_ws_server\test_audio\Slow_Dancing_Layover_[cut_9sec].wav
WAV_FILE = "test_audio/mom.wav"  # 송신 파일 있다고 가정

def send_audio():
    # 서버에 WebSocket 연결
    ws = websocket.create_connection(WS_URL)
    print("✅ WebSocket 연결됨")

    # WAV 파일 열기
    with wave.open(WAV_FILE, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        print("🎧 Frame 길이:", len(frames))  # ← 이거랑 서버에서 받은 바이트 수 비교
        print(f"📤 WAV 데이터 전송: {len(frames)} bytes")
        ws.send_binary(frames)

    # 결과 수신
    result = ws.recv()
    print(f"🧠 서버 응답 (STT 결과): {result}")

    ws.close()

if __name__ == "__main__":
    send_audio()
