import json
from typing import List
from numpy import ceil

from config.config import Config
from tts_project_management.models import AudioData, TtsProject
from tts_project_management.serializer import AudioDataSerializer, TtsProjectSerializer
from exceptions import NotFoundError
from tts_project_management.utils.text_to_speach import GoogleTextToSpeach
from user.models import User
from django.db import transaction
from django.db.models import Q, F


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
    def create_or_update_bulk(self, data: list, project_title: str, slow=False) -> dict():
        bulk_list = []
        self.serializer(data=data)
        # self.serializer.is_valid(raise_exception=True)
        seq = 1
        tts_proj_ins = self.proj_model.objects.get(project_title=project_title)

        audio_config = Config.audio_output
        make_folder = audio_config["make_folder"]

        if make_folder == True:
            self.tts.create_folder(project_title=project_title)

        with transaction.atomic():
            for sentense in data:
                file = self.tts.create_tts(
                    project_title=project_title, text=sentense, slow=slow, sequence=seq
                )
                default = {
                    "text": sentense,
                    "slow": slow,
                    "name": file["name"],
                    "tts_project": tts_proj_ins,
                    "path": file["saved_path"],
                }
                created, is_created = self.model.objects.update_or_create(
                    tts_project=tts_proj_ins, sequence=seq, defaults=default
                )
                temp = self.serializer(created).data
                bulk_list.append(temp)
                seq = seq + 1

        res = dict(zip(range(1, len(bulk_list) + 1), bulk_list))

        return res

    def insert_audio_data(self, project_title: str, data: list, sequence: int, slow=False) -> dict:
        """특정 seq "이후로" 삽입합니다. 만일 뒤에 데이터가 있을경우 숫자만큼 뒤로 밀립니다. 파일명에도 동일 반영됩니다."""
        tts_proj_ins = self.proj_model.objects.get(project_title=project_title)
        bulk_list = []
        self.serializer(data=data)
        # self.serializer.is_valid(raise_exception=True)
        amount = data.count()
        project_id = tts_proj_ins.id

        with transaction.atomic():
            self.push_audio_data(project_id=project_id, amount=amount, seq=seq)
            for sentense in data:
                seq = seq + 1
                file = self.tts.create_tts(
                    project_title=project_title, text=sentense, slow=slow, sequence=seq
                )
                default = {
                    "text": sentense,
                    "slow": slow,
                    "name": file["name"],
                    "tts_project": tts_proj_ins,
                    "path": file["saved_path"],
                }
                created, is_created = self.model.objects.update_or_create(
                    tts_project=tts_proj_ins, sequence=seq, defaults=default
                )
                temp = self.serializer(created).data
                bulk_list.append(temp)
        res = dict(zip(range(1, len(bulk_list) + 1), bulk_list))
        return res

    def push_audio_data(self, project_id: int, amount: int, seq: int) -> None:
        q1 = Q("sequence" > seq)
        q2 = Q("project_id" == project_id)
        q_query = q1.add(q2, Q.AND)
        self.model.objects.filter(q_query).update(sequence=F("sequence") + amount)

    def update_audio_data(self, project_title: str, data: dict, sequence: int) -> dict:
        """project title, 내부 순서 sequence 를 인자로 받아서 프로젝트 내부 sequence번째 오디오 데이터를 업데이트 합니다."""
        file = GoogleTextToSpeach.create_tts(
            project_title=project_title, text=data["text"], slow=data["slow"], sequence=sequence
        )
        updated = (
            self.model.objects.select_related("TtsProject")
            .filter(project_title=project_title, sequence=sequence)
            .update(text=data["text"], speed=data["speed"], name=file["name"], seq_in_proj=sequence)
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
