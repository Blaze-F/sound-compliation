import json
from config.config import config
from tts_project_management.repository import (
    AbstarctAudioDataRepository,
    AbstarctProjectRepository,
    AudioDataRepository,
    TtsProjectRepository,
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
        pass

    def get_page(self, projct_title: str, page=1) -> list():
        """리스트로 반환합니다. 기본 페이지 사이즈 값은 config에 상수로 두었습니다."""
        res = self.tts_project_repo.get_page(project_title=projct_title, page=page)

        return res

    def create_project(self, project_title: str, project_container: list, user_id: int) -> list():

        project = self.tts_project_repo.create(project_title=project_title, user_id=user_id)
        res = self.audio_data_repo.create_bulk(data=project_container, project_title=project_title)
        res["project"] = project
        return res

    def update_project(self, project_title: str, sequense: int, text: str):
        pass

    def delete_project(self, project_title: str) -> str:

        res = self.tts_project_repo.delete(project_title=project_title)
