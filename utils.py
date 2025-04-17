# from pydub import AudioSegment
# import io
# import uuid
# import os
# import tempfile

# def save_audio_temp(audio_bytes: bytes) -> str:
#     """
#     바이트로 받은 오디오 데이터를 임시 wav 파일로 저장하고 경로를 반환한다.
#     - sr: 샘플링 레이트 (Whisper는 16kHz 권장)
#     """
#     try:
#         audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

#         filename = f"{uuid.uuid4().hex}.wav"
#         filepath = os.path.join(tempfile.gettempdir(), filename)

#         audio = audio.set_channels(1).set_frame_rate(16000)  # Whisper 최적화
#         audio.export(filepath, format="wav")

#         return filepath

#     except Exception as e:
#         print(f"[ERROR] 오디오 저장 실패: {e}")
#         return ""

import wave
import uuid
import os
import tempfile
import io

def save_audio_temp(audio_bytes: bytes, sr: int = 16000, sampwidth: int = 2, nchannels: int = 1) -> str:
    """
    raw PCM frames를 정식 .wav 파일로 래핑하여 저장한다
    - sr: 샘플링 레이트 (Hz)
    - sampwidth: 샘플 너비 (바이트), 2 = 16bit
    - nchannels: 채널 수, 1 = Mono
    """
    filename = f"{uuid.uuid4().hex}.wav"
    path = os.path.join(tempfile.gettempdir(), filename)

    try:
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(nchannels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(sr)
            wf.writeframes(audio_bytes)
        return path

    except Exception as e:
        print(f"[❌ WAV 래핑 실패] {e}")
        return ""
