# 🎤 AI 음성 인식 WebSocket 서버 (Unreal 연동용)

> 이 문서는 팀 프로젝트용 STT(WebSocket) 서버를 처음부터 따라할 수 있도록 구성한 **전체 튜토리얼 README**입니다.
>
> **게임(언리얼)**과의 협업 포인트도 함께 안내합니다.

---

## 📁 폴더 구조
```
ai_ws_server/
├── test_audio/                 # 테스트용 음성 wav 파일
│   └── mom.wav
├── client_test.py             # 로컬에서 테스트 가능한 WebSocket 클라이언트
├── main.py                    # FastAPI 기반 WebSocket 서버 (STT 처리 핵심)
├── stt_model.py               # Whisper 모델 로드 및 텍스트 변환 로직
├── utils.py                   # 오디오 저장 도구 (raw → .wav)
├── requirements.txt           # 설치 패키지 목록
└── README.md                # (바로 이 문서)
```

---

## 🌐 시스템 개요

### ✅ 어떤 통신?
- **WebSocket 통신**
- 클라이언트(언리얼 or Python) → 서버로 **음성 프레임 bytes** 전송
- 서버는 Whisper로 **STT 처리 후 텍스트로 응답**

### ✅ 흐름 요약
```
[언리얼 Mic] → 음성 녹음 (raw bytes)
        └──(ws.send_binary) → FastAPI 서버 수신
                            └── Whisper로 텍스트 변환
                                         └── 결과 텍스트 응답
```

---

## ⚙️ 서버 실행법 (FastAPI + Uvicorn)

### 1. 가상환경 생성 (선택)
```bash
conda create -n ws-env python=3.10
conda activate ws-env
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

#### requirements.txt 예시:
```
fastapi
uvicorn
openai-whisper
soundfile
websockets
```

### 3. 서버 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8018 --reload
```

---

## 🧪 테스트 방법 (로컬용 client)

### `client_test.py` 실행
```bash
python client_test.py
```
- 내부에 지정된 `.wav` 파일을 열고
- WebSocket으로 서버에 전송하고
- 응답 텍스트 출력

### 주의사항
- `readframes()`로 가져온 PCM 데이터는 `.wav` 형식이 아님
- 서버에서 `utils.py`로 **헤더 추가 래핑 후 저장** 필요 (이 프로젝트는 이미 구현됨)

---

## 🕹️ 게임반 요청사항 (언리얼 측 작업)

### 🎯 Unreal이 해야 할 것
- 마이크 입력을 통해 **raw PCM bytes** 획득
- WebSocket으로 **binary 형식 전송**
- 수신된 텍스트를 HUD, 퀘스트 시스템 등에 연결

### 📩 보내는 방식 명세 (언리얼 → 서버)
- WebSocket URL: `ws://<서버 IP>:8018/ws/audio`
- 데이터 타입: `binary`
- 전송 내용: `16bit / 16kHz / mono` 기준의 **raw PCM bytes**

### 📬 받는 형식 (서버 → 언리얼)
- `text` 메시지 1개
- 인식된 문장이 그대로 들어감

### 예시 흐름
```json
[Send]  binary: b'\x1a\x32...'
[Recv]  text:   "정답은 청개구리입니다."
```

---

## 🔍 디버깅 팁

### 서버에서 받은 파일 직접 확인
- `main.py` 안에 저장된 `debug_XXXX.wav` 를 들어보면 깨졌는지 판단 가능
- 정상 재생 안되면 언리얼 쪽 전송 문제 가능성 높음

### Whisper가 "인식 실패"만 내놓는다면?
- 전송된 데이터가 깨졌을 가능성 높음
- 헤더 없는 raw를 `.wav`로 변환하는 과정 (`utils.py`) 확인 필요

---

## ✅ 이 프로젝트의 목적 요약
| 항목 | 설명 |
|------|------|
| 목표 | 실시간 STT를 게임에 접목시키기 위한 백엔드 서버 구축 |
| 방식 | WebSocket 기반 통신, Whisper STT 모델 활용 |
| 입력 | 언리얼 또는 클라에서 전송한 음성 데이터 (raw PCM) |
| 출력 | 인식된 텍스트 문자열 1줄 |

---

## 👥 팀원 전달 시 요약
> "이 서버는 음성 데이터를 WebSocket으로 받으면 Whisper로 STT 처리해서 텍스트를 돌려주는 백엔드야. 언리얼 쪽은 마이크로 받은 raw PCM을 binary로 전송만 해줘."

---

## 🔗 참고
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [FastAPI WebSocket Docs](https://fastapi.tiangolo.com/advanced/websockets/)

