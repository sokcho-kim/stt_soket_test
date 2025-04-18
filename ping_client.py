import asyncio
import websockets
import struct
import time

async def ping_pong():
    uri = "ws://localhost:8000/ws"  # 서버 주소

    # 구성값
    msg_type = 1  # Ping
    payload_size = 8
    session_id = "test-session".encode().ljust(100, b"\x00")
    player_id = 42
    timestamp = time.time()

    # 패킷 만들기
    header = struct.pack("!BH", msg_type, payload_size) + session_id + struct.pack("!B", player_id)
    body = struct.pack("!d", timestamp)
    packet = header + body  # 112 bytes

    async with websockets.connect(uri) as ws:
        print("📤 Ping 전송")
        await ws.send(packet)

        pong = await ws.recv()
        pong_type, pong_payload = struct.unpack("!BH", pong[:3])
        pong_time = struct.unpack("!d", pong[104:112])[0]
        print(f"📥 Pong 수신: Type={pong_type}, Timestamp={pong_time}")

if __name__ == "__main__":
    asyncio.run(ping_pong())
