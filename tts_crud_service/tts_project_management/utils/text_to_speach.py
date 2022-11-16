from gtts import gTTS

from config.config import config


class GoogleTextToSpeach:
    def __init__(self) -> None:
        pass

    def create_tts(self, text: str, sequense: int, slow: bool, project_title: str) -> dict:
        """TTS mp3 파일을 생성해서 생성정보를 리턴합니다.
        파일 명명규칙 : f"audio_outputs\{project_title}_{text}_{str(sequense).zfill(3)}.mp3"
        생성경로 .audio_outputs\ """
        tts = gTTS(text=text, slow=slow, lang="ko")

        tts.save(f"audio_outputs\GTTS_{project_title}_{text}_{str(sequense).zfill(3)}.mp3")

        # TODO SavedPath Config에서 인수로 받아오기.
        data = {
            "sequense": sequense,
            "name": f"GTTS_{text}_{str(sequense).zfill(3)}",
            "saved_path": f"audio_outputs\GTTS_{project_title}_{text}_{str(sequense).zfill(3)}",
        }
        return data
