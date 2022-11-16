from gtts import gTTS

from config.config import config
import os


class GoogleTextToSpeach:
    def __init__(self) -> None:
        pass

    def create_tts(self, text: str, sequence: int, slow: bool, project_title: str) -> dict:
        """TTS mp3 파일을 생성해서 생성정보를 리턴합니다.
        파일 명명규칙 : GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3
        경로 및 폴더 생성 관련 설정 config 파일에 있습니다.
        텍스트에 물음표가 포함된경우 내용은 정상반영되지만 파일명에는 나타나지 않습니다."""
        tts = gTTS(text=text, slow=slow, lang="ko")
        project_folder = ""
        # 이름에 ? 들어가면 에러가 발생
        text = text.replace("?", "")
        audio_config = config.audio_output
        make_folder = audio_config["make_folder"]
        save_path = audio_config["path"]

        if make_folder == True:
            project_folder = f"{project_title}/"

        tts.save(
            f"{save_path}{project_folder}GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3"
        )

        data = {
            "sequence": sequence,
            "name": f"GTTS_{project_title}_{str(sequence).zfill(3)}_{text}",
            "saved_path": f"{save_path}{project_folder}GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3",
        }

        return data

    def create_folder(self, project_title: str):

        audio_config = config.audio_output
        save_path = audio_config["path"]

        temp = f"{save_path}{project_title}"

        try:
            if not os.path.exists(f"{save_path}{project_title}"):
                os.makedirs(f"{save_path}{project_title}")
        except OSError:
            raise print("Error: Creating directory. " + temp)
