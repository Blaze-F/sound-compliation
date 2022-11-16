import json
from config.config import config
from tts_project_management.repository import (
    AbstarctAudioDataRepository,
    AbstarctProjectRepository,
)


class TtsProjectManagementService:
    def __init__(
        self,
        tts_project_repo: AbstarctProjectRepository,
        audio_data_repo: AbstarctAudioDataRepository,
    ) -> None:
        # TODO self 변수로 받기
        self.tts_project_repo = tts_project_repo
        self.audio_data_repo = audio_data_repo

    def get_page(self, projct_title: str, page=1) -> list():
        """리스트로 반환합니다. 기본 페이지 사이즈 값은 config에 상수로 두었습니다."""
        res = self.tts_project_repo.get_page(project_title=projct_title, page=page)

        return res

    def create_project(self, project_title: str, project_container: list, user_id: int) -> dict:

        project = self.tts_project_repo.create(project_title=project_title, user_id=user_id)
        res = self.audio_data_repo.create_or_update_bulk(
            data=project_container, project_title=project_title
        )
        res["project"] = project
        return res

    def delete_project(self, project_title: str) -> str:
        res = self.tts_project_repo.delete(project_title=project_title)


class AudioDataManagementService:
    def __init__(
        self,
        tts_project_repo: AbstarctProjectRepository,
        audio_data_repo: AbstarctAudioDataRepository,
    ) -> None:
        # TODO self 변수로 받기
        self.tts_project_repo = tts_project_repo
        self.audio_data_repo = audio_data_repo

    def insert_audio_data(self, project_title: str, data: list, sequence: int, slow=False) -> dict:
        res = self.audio_data_repo.insert_audio_data(
            project_title=project_title, data=data, sequence=sequence
        )
        return res

    def update_audio_data(
        self, project_title: str, sentense: str, sequence: int, slow=False
    ) -> dict:
        res = self.audio_data_repo.update_audio_data(
            project_title=project_title, sentense=sentense, sequence=sequence, slow=slow
        )
        return res

    def delete_audio_data(
        self, project_title: str, sequence: int, delete_amount: int, user_id: int
    ) -> str:
        """해당 seq에 해당하는 audio 데이터를 삭제합니다."""
        self.audio_data_repo.delete_audio_data_sequence(
            project_title=project_title, sequence=sequence
        )
        msg = f"{project_title}_{sequence}delete completed."
        return msg
