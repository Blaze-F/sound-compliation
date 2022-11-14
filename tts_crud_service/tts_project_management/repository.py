from tts_project_management.models import AudioData, TtsProjects
from tts_project_management.serializer import AudioDataSerializer, TtsProjectSerializer
from exceptions import InvalidRequestError, NotAuthorizedError, NotFoundError


class AbstarctProjectRepository:
    def __init__(self) -> None:
        self.model = TtsProjects
        self.serializer = TtsProjectSerializer


class TtsProjectRepository(AbstarctProjectRepository):
    def create(self, project_title: str) -> dict:
        obj = self.model.objects.create(project_title=project_title)
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


class AbstarctAudioDataRepository:
    def __init__(self) -> None:
        self.model = AudioData
        self.serializer = AudioDataSerializer


class AudioDataRepository(AbstarctAudioDataRepository):
    def create(self, data: dict, tts_project_id: int) -> dict:

        self.serializer(data=data)
        self.serializer.is_valid(raise_exception=True)

        created = self.model.objects.create(
            text=data["text"], speed=data["speed"], data="", tts_project=tts_project_id
        )
        return self.serializer(created).data

    def update(self, data: dict, audio_id: int) -> dict:
        updated = self.model.objects.filter(id=audio_id).update(
            text=data["text"],
            speed=data["speed"],
        )
        return updated

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return "delete"

    def get(self, audio_id: int):
        get = self.model.objects.get(id=audio_id)
        # TODO
        try:
            return self.serializer(get).data
        except self.model.DoesNotExist:
            raise NotFoundError
