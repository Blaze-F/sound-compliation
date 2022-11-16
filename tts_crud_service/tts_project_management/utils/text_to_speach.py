from gtts import gTTS

from config.config import config
import os


class GoogleTextToSpeach:
    def __init__(self) -> None:
        pass

    def create_tts(self, text: str, sequense: int, slow: bool, project_title: str) -> dict:
        """TTS mp3 파일을 생성해서 생성정보를 리턴합니다.
        파일 명명규칙 : GTTS_{project_title}_{str(sequense).zfill(3)}_{text}.mp3
        경로 및 폴더 생성 관련 설정 config 파일에 있습니다."""
        tts = gTTS(text=text, slow=slow, lang="ko")
        project_folder = ""

        audio_config = config.audio_output
        make_folder = audio_config["make_folder"]
        save_path = audio_config["path"]

        if make_folder == True:
            project_folder = f"{project_title}/"

        tts.save(
            f"{save_path}{project_folder}GTTS_{project_title}_{str(sequense).zfill(3)}_{text}.mp3"
        )

        data = {
            "sequense": sequense,
            "name": f"GTTS_{project_title}_{text}_{str(sequense).zfill(3)}",
            "saved_path": f"{save_path}{project_folder}GTTS_{project_title}_{str(sequense).zfill(3)}_{text}.mp3",
        }

        return data

    def create_folder(project_title: str):

        audio_config = config.audio_output
        save_path = audio_config["path"]

        temp = f"{save_path}{project_title}"

        try:
            if not os.path.exists(f"{save_path}{project_title}"):
                os.makedirs(f"{save_path}{project_title}")
        except OSError:
            raise print("Error: Creating directory. " + temp)
