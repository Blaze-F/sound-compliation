import json
from typing import List
from numpy import ceil
from config.config import Config
from tts_project_management.models import AudioData, TtsProject
from tts_project_management.serializer import AudioDataSerializer, TtsProjectSerializer
from exceptions import NotFoundError
from tts_project_management.utils.text_to_speach import GoogleTextToSpeach
from user.models import User


class AbstarctProjectRepository:
    def __init__(self) -> None:
        self.model = TtsProject
        self.serializer = TtsProjectSerializer
        self.audio_data_serializer = AudioDataSerializer
        self.audio_data_repository = AudioDataRepository()
        self.user = User


class TtsProjectRepository(AbstarctProjectRepository):
    # TODO 업데이트, create 나누기
    def create(self, project_title: str, user_id: int) -> dict:
        user_ins = self.user.objects.get(id=user_id)
        default = {"user": user_ins}
        obj, is_created = self.model.objects.update_or_create(
            project_title=project_title, defaults=default
        )
        try:
            return self.serializer(obj).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_title(self, project_title: str) -> dict:
        obj = self.model.objects.get(project_title=project_title)
        try:
            return self.serializer(obj).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_page(self, project_title: str, page: int) -> list():
        """리스트로 반환합니다. 기본 페이지 값은 config에 상수로 두었습니다."""
        page_size = Config.pagenation["page_size"]
        limit = page_size * int(page)
        offset = limit - page_size
        try:
            proj = self.model.objects.get(project_title=project_title)
            data = self.serializer(proj)
            cnt = data["audio_data_count"]
            page_audio_data = data.audio_data_set
            # page_audio_data = obj.text_set.all().order_by("index")[offset:limit]

            page_count = ceil(cnt / page_size)
            context = [{"page": page, "page_count": page_count}]
            return data, context
        except self.model.DoesNotExist:
            raise NotFoundError

    def delete(self, project_title: str) -> str:
        entity = self.model.objects.get(project_title=project_title)
        proj_id = entity.id
        entity.delete()
        return f"deleted{proj_id}"


class AbstarctAudioDataRepository:
    def __init__(self) -> None:
        self.model = AudioData
        self.serializer = AudioDataSerializer
        self.tts_project_repo = TtsProjectRepository
        self.proj_model = TtsProject
        self.tts = GoogleTextToSpeach()


class AudioDataRepository(AbstarctAudioDataRepository):
    def create(self, data: dict, tts_project_id: int, sequense: int) -> dict:

        self.serializer(data=data)
        self.serializer.is_valid(raise_exception=True)

        file = GoogleTextToSpeach.create_tts(
            text=data["text"], slow=data["slow"], sequense=sequense
        )
        created = self.model.objects.create(
            text=data["text"],
            slow=data["slow"],
            name=file["name"],
            tts_project=tts_project_id,
            seq_in_proj=sequense,
        )
        return self.serializer(created).data

    def create_bulk(self, data: list, project_title: str, slow=False) -> dict():
        bulk_list = []
        self.serializer(data=data)
        # self.serializer.is_valid(raise_exception=True)
        seq = 0
        tts_proj_ins = self.proj_model.objects.get(project_title=project_title)
        for sentense in data:

            file = self.tts.create_tts(
                project_title=project_title, text=sentense, slow=slow, sequense=seq
            )
            created = self.model.objects.create(
                text=sentense,
                slow=slow,
                name=file["name"],
                tts_project=tts_proj_ins,
                sequense=seq,
                path=file["saved_path"],
            )
            temp = self.serializer(created).data
            bulk_list.append(temp)
            seq = seq + 1

        res = dict(zip(range(1, len(bulk_list) + 1), bulk_list))

        return res

    def update_audio_data(self, project_title: str, data: dict, sequense: int) -> dict:
        """project title, 내부 순서 sequence 를 인자로 받아서 프로젝트 내부 sequence번째 오디오 데이터를 업데이트 합니다."""
        file = GoogleTextToSpeach.create_tts(
            project_title=project_title, text=data["text"], slow=data["slow"], sequense=sequense
        )
        updated = (
            self.model.objects.select_related("TtsProject")
            .filter(project_title=project_title, sequense=sequense)
            .update(text=data["text"], speed=data["speed"], name=file["name"], seq_in_proj=sequense)
        )
        try:
            return self.serializer(updated).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get(self, audio_id: int):
        get = self.model.objects.get(id=audio_id)
        # TODO
        try:
            return self.serializer(get).data
        except self.model.DoesNotExist:
            raise NotFoundError
