import datetime
from unittest import mock
from django.conf import settings
import pytest
from exceptions import NotFoundError
from tts_project_management.models import AudioData, TtsProject
from tts_project_management.repository import AudioDataRepository, TtsProjectRepository
from tts_project_management.service import AudioDataManagementService, TtsProjectManagementService
from tts_project_management.utils.preprocess import Preprocessor

from datetime import datetime, timedelta, timezone

# 인스턴스 생성
tts_project_repository = TtsProjectRepository()
audio_data_repository = AudioDataRepository()
service = TtsProjectManagementService(
    tts_project_repo=tts_project_repository, audio_data_repo=audio_data_repository
)
audio_service = AudioDataManagementService(
    tts_project_repo=tts_project_repository, audio_data_repo=audio_data_repository
)
preprocessor = Preprocessor()

mock_tts_return_data = {
    "sequence": 2,
    "name": "GTTS_{project_title}_{str(sequence).zfill(3)}_{text}",
    "saved_path": "{save_path}{project_folder}GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3",
}

datetime_utc = datetime.utcnow()
timezone_kst = timezone(timedelta(hours=9))
datetime_kst = datetime_utc.astimezone(timezone_kst)


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create():
    # given
    data = {
        "project_title": "테스트 프로젝트",
        "sentense": "걔는 진짜 딱 오잖아? 지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지?이게 모 몰려있잖아 아침에 버스정류장이 지금처럼 이렇게 잘 돼 있지 않아 지금처럼 이렇게 뻐드렁?이렇게 있어가지고 딱 한 줄 서기 그런 게 아니고 이 동인천역 앞에 동인천역 앞에 그냥 뭉탱이로 있단 말야, 그러면은 이러고 있다가 버스가 어디에서 여 앞 쪽에서 올지 뒷 쪽에서 눈치를 봐야 돼. 이렇게 뭉탱이로 이르케 흐트러져 있다가 뭐 44번 버스가 온다 그러면은 그니까 가거든? 그러면 사람들이 가잖아. 그럼 다들 이렇게 눈치껏 이렇게 하고 대충 이 쯤에 열린다고 하면은 뭐 나보다 앞에 있으면 이 사람이 먼저 나오는데, 걔는 하면은 이런다? 이러고 사람이 갈려고 그러잖아? 그럼 이러면서 한다? 아르테미스 1호 미션의 개념은 SLS 개발 당시 '탐험미션-1 (Exploration Mission-1)'이란 명칭으로 추진된 비행 임무에서 비롯되었다.",
    }
    # when
    temp = data["sentense"]
    sentense = preprocessor.preprocess_data(data["sentense"])
    res = service.create_project(
        project_container=sentense, project_title=data["project_title"], user_id=1
    )
    # then
    assert isinstance(res, dict)


@pytest.mark.django_db()
def test_pagination():
    context, serialized = service.get_page(1, 1)
    assert isinstance(context, list), isinstance(serialized, dict)


@pytest.mark.django_db()
@mock.patch(
    "tts_project_management.utils.text_to_speach.GoogleTextToSpeach.rename_tts_sequence",
    return_value=None,
)
def test_insert_sentense(self):
    # given
    project = TtsProject(
        id=1,
        project_title="테스트 프로젝트",
        user_id=1,
        created_at=datetime_kst,
        updated_at=datetime_kst,
    )
    project.save()
    data = {
        "project_title": "테스트 프로젝트",
        "sentense": "테스트용 문장 입니다. 테스트용 문장 2 입니다.",
    }
    sentense = preprocessor.preprocess_data(data["sentense"])

    # when
    res = audio_service.insert_audio_data(
        project_title=data["project_title"], data=sentense, sequence=2
    )

    # then
    assert isinstance(res, dict)


# mock 있을때만 self
@pytest.mark.django_db()
@mock.patch(
    "tts_project_management.utils.text_to_speach.GoogleTextToSpeach.create_tts",
    return_value=mock_tts_return_data,
)
def test_update_audio_data(self):
    # given
    project = TtsProject(
        id=1,
        project_title="테스트 프로젝트",
        user_id=1,
        created_at=datetime_kst,
        updated_at=datetime_kst,
    )
    project.save()

    data = {
        "project_title": "테스트 프로젝트",
        "sentense": "최대 문장길이는 100자입니다.",
    }

    # when
    res = audio_service.update_audio_data(
        project_title=data["project_title"], sentense=data["sentense"], sequence=2
    )

    # then
    assert isinstance(res, dict)


@pytest.mark.django_db()
def test_delete_audio_data():
    # given
    project = TtsProject(
        id=2,
        project_title="테스트 프로젝트2",
        user_id=1,
        created_at=datetime_kst,
        updated_at=datetime_kst,
    )
    project.save()
    audio_data = AudioData(
        id=4,
        tts_project=project,
        created_at=datetime_kst,
        updated_at=datetime_kst,
        text="text",
        name="name",
        path="path",
        sequence=1,
        slow=False,
    )
    audio_data.save()

    # when
    res = audio_service.delete_audio_data(project_title="테스트 프로젝트2", sequence=1)

    # then
    assert isinstance(res, str)


@pytest.mark.django_db()
def test_delete_project():
    # given
    project = TtsProject(
        id=3,
        project_title="테스트 프로젝트3",
        user_id=1,
        created_at=datetime_kst,
        updated_at=datetime_kst,
    )
    project.save()
    audio_data = AudioData(
        id=2,
        tts_project=project,
        created_at=datetime_kst,
        updated_at=datetime_kst,
        text="text",
        name="name",
        path="path",
        sequence=1,
        slow=False,
    )
    audio_data.save()

    # when
    res = service.delete_project(project_title="테스트 프로젝트3")

    # then
    assert isinstance(res, str)
