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

    def rename_tts_sequence(self, addnum: int, past_name_list: list, project_title: str):
        """_을 기준으로 파일명을 split 합니다. 프로젝트명, 등 다른 변수에 _가 들어갈경우 에러 가능성이 있습니다."""
        # TODO 정규표현식 적용 알아보기
        audio_config = config.audio_output
        save_path = audio_config["path"]
        make_folder = audio_config["make_folder"]

        if make_folder == True:
            project_path = f"{save_path}{project_title}"
        else:
            project_path = f"{save_path}"

        for data in past_name_list:
            splited = data["name"].split("_")
            past_seq = int(splited[2])
            new_seq = past_seq + addnum
            new_name_seq = str(new_seq).zfill(3)
            os.rename(
                project_path
                + data["name"]
                + f"{project_path}GTTS_{splited[1]}_{new_name_seq}_{splited[3]}.mp3"
            )
