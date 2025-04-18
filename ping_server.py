import struct
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 WebSocket 연결됨")

    try:
        while True:
            data = await websocket.receive_bytes()
            if len(data) != 112:
                print("❌ 잘못된 패킷 크기:", len(data))
                continue

            # Header (104 bytes) + Timestamp (8 bytes)
            header_bytes = data[:104]
            timestamp_bytes = data[104:]

            # 헤더 파싱
            msg_type, payload_size = struct.unpack("!BH", header_bytes[:3])
            session_id = header_bytes[3:103].decode(errors="ignore").strip("\x00")
            player_id = header_bytes[103]

            print(f"📩 수신: Type={msg_type}, Size={payload_size}, SessionID={session_id}, PlayerID={player_id}")

            if msg_type == 1:  # Ping
                timestamp = struct.unpack("!d", timestamp_bytes)[0]
                print(f"⏱️ Timestamp: {timestamp}")

                # 응답용 패킷 구성 (Header + Timestamp)
                response = b""
                response += struct.pack("!BH", 2, 8)                            # Type = 2 (Pong), Payload = 8
                response += struct.pack("100s", bytes(session_id.ljust(100), "utf-8"))
                response += struct.pack("!B", player_id)
                response += struct.pack("!d", timestamp)

                await websocket.send_bytes(response)
                print("📤 Pong 전송 완료")

    except Exception as e:
        print("❌ 오류:", e)
