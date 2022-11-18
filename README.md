# Making TTS Project

문장이 주어졌을때 이를 전처리하여 TTS 음성파일을 만들고 그 정보를 관리하는 API

</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [🛠 개발 조건](#-개발-조건)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [실행방법-&-한번-확인해주세요!](#실행방법--한번-확인해주세요)
      - [Config](#config)
  * [API ENDPOINT](#api-endpoint)
  * [상세한 설명](#상세-설명)
  * [프로젝트 후기](#프로젝트-후기)


## 프로젝트 개요
#### 💭 프로젝트 설명
#### 🛠 개발 조건

 - 프로젝트 생성(오디오 생성)
    - 텍스트(str)가 담긴 리스트를 받습니다. (length = 1)
    - 이를 전처리하여 오디오를 생성하는 함수의 input으로 같이 넣습니다.
    - [['text1', 'text2', 'text3', ....], path]
    - 일정시간 이후 함수에서 (id, text)형태의 원소를 가진 리스트를 리턴합니다.
    - [('id1' ,'text1'), ('id2', 'text2'), ('id3', 'text3'), ....]
    - 오디오는 input의 path에 저장됩니다.
  - 텍스트 조회
    - 특정 프로젝트의 n번째 페이지를 조회합니다.
    - 한페이지는 10문장으로 이루어져 있습니다.
  - 텍스트 수정
    - 한 문장의 텍스트와 스피드를 수정합니다.
    - 텍스트(오디오) 생성 / 삭제
    - 삽입위치는 항상 앞, 뒤가 아닌 중간도 가능.
  -프로젝트 삭제

#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST Framework
- **Database** : Mysql

</br>



#### 📰 모델링
![tts_project](https://user-images.githubusercontent.com/101803254/202617042-abbb6490-8c94-4366-a8b8-82bbd0b2f791.png)

</br>

#### 🛠 API Test

- 이번 프로젝트의 경우 Service 단이 그렇게 비대해지지는 않았기에 Serivce To Repo Test로 한번에 작성
![2022-11-17 17 50 29](https://user-images.githubusercontent.com/101803254/202606449-10f26810-8178-4786-91c4-e3b260b23754.png)

테스트 커버리지는 2022-11-17 현재 88.4% 입니다.

확인방법:
```
pytest --cov
```

</br>

## 프로젝트 분석
![제목 없는 다이어그램](https://user-images.githubusercontent.com/101803254/202605476-ae90f7da-6548-4582-b99b-4dbdb975fdb3.jpg)

- DB와 직결되는 모델이 실제 비즈니스 레이어, View 까지 넘어가지 않고 중간에 직렬화를 한번 거치게 함으로써 DB와 모델의 무결성을 보장하였음
- 기존 MVC 패턴에서 너무 한쪽이 비대하지고 책임이 불분명해지는걸 막기위해 클래스들을 나누고 추상클래스, 상속 등을 통해 의존성과 결합도를 낮추고 단위 테스트를 용이하게 함.

</br>

## 실행방법 & 한번 확인해주세요!

### Config_example.yml
실제 파일은 Config.yml 입니다.
```yml
databases:
  host: "localhost"
  port: 3306
  database: "tts_service"
  username: "db user name"
  password: "db pw"
  timezone: "+09:00"

secrets:
  django: "django secret"

token:
  secret: "jwt secret"
  expire_sec: 3600

pagenation:
  default_page_size: 10

audio_output:
  #끝에 /포함해주세요
  path: "audio_outputs/"
  #프로젝트 이름으로 된 폴더를 생성하여 음성 데이터를 저장할지 여부를 나타냅니다.
  make_folder: True
```

### RUN
> ```
>pip install requirements.txt
>python manage.py makemigrations
>python manage.py migrate
>python manage.py runserver
>```
## API ENDPOINT

### user

URL|Method|Description|
|------|---|---|
|"signup/"|POST|회원가입|
|"login/"|POST|로그인 : access Token 이 반환되며 헤더에 추가해야 하위 기능들을 이용하실 수 있습니다.|


### project

URL|Method|Description|
|------|---|---|
|"project/"|POST|프로젝트, 오디오 생성 (login Required: 로그인이 필수입니다.)|
|"project/?project_id=1&page=1"|GET| 프로젝트 정보 (페이징) (login Required: 로그인이 필수입니다.)|
|"project/"|DELETE|프로젝트 삭제 (Owner Check: 소유자를 검사합니다.)| 
|"project/audio/update"|PUT|오디오 데이터 업데이트 (Owner Check: 소유자를 검사합니다.)|
|"project/push"|PUT|문장단위 삽입 (Owner Check: 소유자를 검사합니다.)| 
|"/project/audio/delete"|DELETE| 오디오 데이터 삭제 (Owner Check: 소유자를 검사합니다.)| 

##API Req, Res 예제, 상세설명

## /signup/ (POST)
### Request
 ```json
{
    "name": "사람이름",
    "email": "kinggod2@gmail.com",
    "password": "test1234"
}
 ```
   
### Response
    
 ```json
 {
    "id": 16,
    "created_at": "2022-11-18T03:28:21.153322Z",
    "updated_at": "2022-11-18T03:28:21.153322Z",
    "name": "사람이름",
    "email": "kinggod2@gmail.com",
    "password": "$2b$12$hMAMwrTSzulud/zWMBaLee9f/czjVuwy7FgRayQLEClBXmMkM52bq"
}
```

## /logini/ (POST)
### Request
 ```json
{
    "email": "kinggod@gmail.com",
    "password": "test1234"
}

 ```
   
### Response
    
 ```json
{
    "access": "accessToken"
}
```


## /project/ (POST) (login Required)

### Request
 ```json
 {
    "project_title": "그냥 프로젝트",
    "sentenses": "걔는 진짜 딱 오잖아? 지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지?이게 모 몰려있잖아 아침에 버스정류장이 지금처럼 이렇게 잘 돼 있지 않아 지금처럼 이렇게 뻐드렁?이렇게 있어가지고 딱 한 줄 서기 그런 게 아니고 이 동인천역 앞에 동인천역 앞에 그냥 뭉탱이로 있단 말야, 그러면은 이러고 있다가 버스가 어디에서 여 앞 쪽에서 올지 뒷 쪽에서 눈치를 봐야 돼. 이렇게 뭉탱이로 이르케 흐트러져 있다가 뭐 44번 버스가 온다 그러면은 그니까 가거든? 그러면 사람들이 가잖아. 그럼 다들 이렇게 눈치껏 이렇게 하고 대충 이 쯤에 열린다고 하면은 뭐 나보다 앞에 있으면 이 사람이 먼저 나오는데, 걔는 하면은 이런다? 이러고 사람이 갈려고 그러잖아? 그럼 이러면서 한다? 아르테미스 1호 미션의 개념은 SLS 개발 당시 '탐험미션-1 (Exploration Mission-1)'이란 명칭으로 추진된 비행 임무에서 비롯되었다. 당시 계획은 2017년까지 오리온 우주선을 탑재한 SLS 로켓의 첫 발사를 수행하는 것이었다. 이후 2019년 5월 트럼프 행정부가 유인 달 탐사 계획 아르테미스 계획을 발표하면서 탐험미션-1은 '아르테미스 1호'로 개칭되었다. 당시 예정된 일정은 2020년 11월 발사였다.사용 로켓은 SLS 로켓으로 정해졌으나 SLS의 개발 지연으로 한때 스페이스X의 팰컨 헤비나 ULA의 델타 IV 헤비의 사용이 거론된 적도 있었다. 하지만 NASA에서 2019년 11월 말 SLS 코어를 완성하였고 12월에는 내구도 테스트까지 성공하면서 SLS 사용이 기정사실화되었다."
}
 ```
### Response
    
 ```json
 {
    "1": {
        "id": 19,
        "created_at": "2022-11-17T05:00:30.909545Z",
        "updated_at": "2022-11-18T03:29:29.362512Z",
        "text": "걔는 진짜 딱 오잖아?",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_001_걔는 진짜 딱 오잖아？",
        "sequence": 1,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_001_걔는 진짜 딱 오잖아？.mp3",
        "tts_project": 2
    },
    "2": {
        "id": 20,
        "created_at": "2022-11-17T05:00:31.387540Z",
        "updated_at": "2022-11-18T03:29:29.841181Z",
        "text": "지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지?",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_002_지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지？",
        "sequence": 2,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_002_지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지？.mp3",
        "tts_project": 2
    },
    ...
    "14": {
        "id": 32,
        "created_at": "2022-11-17T05:00:37.346010Z",
        "updated_at": "2022-11-18T03:29:35.698903Z",
        "text": "사용 로켓은 SLS 로켓으로 정해졌으나 SLS의 개발 지연으로 한때 스페이스X의 팰컨 헤비나 ULA의 델타 IV 헤비의 사용이 거론된 적도 있었다.",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_014_사용 로켓은 SLS 로켓으로 정해졌으나 SLS의 개발 지연으로 한때 스페이스X의 팰컨 헤비나 ULA의 델타 IV 헤비의 사용이 거론된 적도 있었다.",
        "sequence": 14,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_014_사용 로켓은 SLS 로켓으로 정해졌으나 SLS의 개발 지연으로 한때 스페이스X의 팰컨 헤비나 ULA의 델타 IV 헤비의 사용이 거론된 적도 있었다..mp3",
        "tts_project": 2
    },
    "15": {
        "id": 33,
        "created_at": "2022-11-17T05:00:37.935329Z",
        "updated_at": "2022-11-18T03:29:36.213485Z",
        "text": "하지만 NASA에서 2019년 11월 말 SLS 코어를 완성하였고 12월에는 내구도 테스트까지 성공하면서 SLS 사용이 기정사실화되었다.",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_015_하지만 NASA에서 2019년 11월 말 SLS 코어를 완성하였고 12월에는 내구도 테스트까지 성공하면서 SLS 사용이 기정사실화되었다.",
        "sequence": 15,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_015_하지만 NASA에서 2019년 11월 말 SLS 코어를 완성하였고 12월에는 내구도 테스트까지 성공하면서 SLS 사용이 기정사실화되었다..mp3",
        "tts_project": 2
    },
    "project": {
        "id": 2,
        "created_at": "2022-11-17T05:00:30.553698Z",
        "updated_at": "2022-11-18T03:29:29.008655Z",
        "project_title": "그냥 프로젝트",
        "user": 1
    }
}
```
![image](https://user-images.githubusercontent.com/101803254/202610603-5559f727-0672-4f0b-bb6a-9ce641123724.png)
설정된 경로에 파일이 실제로 생성됩니다. TTS 는 GTTS를 사용했습니다.
파일 명명규칙 : GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3
입니다.

텍스트에 물음표가 포함된경우 파일 이름 에러로 인해 "？"특수문자 U+ff1f 물음표로 대치시켜 저장합니다.
### utills/text_to_speach.py/GoogleTextToSpeach
```python
 def create_tts(self, text: str, sequence: int, slow: bool, project_title: str) -> dict:
        """TTS mp3 파일을 생성해서 생성정보를 리턴합니다.
        파일 명명규칙 : GTTS_{project_title}_{str(sequence).zfill(3)}_{text}.mp3
        경로 및 폴더 생성 관련 설정 config 파일에 있습니다.
        텍스트에 물음표가 포함된경우 파일 이름 에러로 인해 "？"특수문자 U+ff1f 물음표로 대치시켜 저장합니다."""
        tts = gTTS(text=text, slow=slow, lang="ko")
        project_folder = ""
        text = text.replace("?", "？")
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
```

## project/?project_id=1&page=1 (GET) (login Required)

### Request
 ```json
 ```
   
### Response
 ```json
{
    "page_info": [
        {
            "page": "1",
            "page_count": 2.0
        }
    ],
    "data": [
        {
            "id": 19,
            "created_at": "2022-11-17T05:00:30.909545Z",
            "updated_at": "2022-11-18T03:29:29.362512Z",
            "text": "걔는 진짜 딱 오잖아?",
            "slow": false,
            "name": "GTTS_그냥 프로젝트_001_걔는 진짜 딱 오잖아？",
            "sequence": 1,
            "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_001_걔는 진짜 딱 오잖아？.mp3",
            "tts_project": 2
        },
        {
            "id": 20,
            "created_at": "2022-11-17T05:00:31.387540Z",
            "updated_at": "2022-11-18T03:29:29.841181Z",
            "text": "지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지?",
            "slow": false,
            "name": "GTTS_그냥 프로젝트_002_지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지？",
            "sequence": 2,
            "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_002_지 혼자 이케가지고 진짜 이러면서 막 새치기하면서 들어가고 어우 진짜 뭐 뭐 뭔 느낌인지 알지？.mp3",
            "tts_project": 2
        },
        ...
          {
            "id": 26,
            "created_at": "2022-11-17T05:00:34.436298Z",
            "updated_at": "2022-11-18T03:29:32.921910Z",
            "text": "이러고 사람이 갈려고 그러잖아?",
            "slow": false,
            "name": "GTTS_그냥 프로젝트_008_이러고 사람이 갈려고 그러잖아？",
            "sequence": 8,
            "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_008_이러고 사람이 갈려고 그러잖아？.mp3",
            "tts_project": 2
        },
        {
            "id": 27,
            "created_at": "2022-11-17T05:00:34.715786Z",
            "updated_at": "2022-11-18T03:29:33.212739Z",
            "text": "그럼 이러면서 한다?",
            "slow": false,
            "name": "GTTS_그냥 프로젝트_009_그럼 이러면서 한다？",
            "sequence": 9,
            "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_009_그럼 이러면서 한다？.mp3",
            "tts_project": 2
        },
        {
            "id": 28,
            "created_at": "2022-11-17T05:00:35.310878Z",
            "updated_at": "2022-11-18T03:29:33.702675Z",
            "text": "아르테미스 1호 미션의 개념은 SLS 개발 당시 탐험미션1 Exploration Mission1이란 명칭으로 추진된 비행 임무에서 비롯되었다.",
            "slow": false,
            "name": "GTTS_그냥 프로젝트_010_아르테미스 1호 미션의 개념은 SLS 개발 당시 탐험미션1 Exploration Mission1이란 명칭으로 추진된 비행 임무에서 비롯되었다.",
            "sequence": 10,
            "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_010_아르테미스 1호 미션의 개념은 SLS 개발 당시 탐험미션1 Exploration Mission1이란 명칭으로 추진된 비행 임무에서 비롯되었다..mp3",
            "tts_project": 2
        }
    ]
}
```
페이징 단위 10 즉 10번 Sequence 까지 조회됩니다. 

## /project/push (POST) (Owner Check: 소유자를 검사합니다.)

### Request
 ```json
 {
    "project_title": "그냥 프로젝트",
    "sentenses":"전처리. 하실수있도록. 새롭게? 삽입된 문장입니다!",
    "sequence":2
}
 ```
   
### Response
 ```json
 {
    "1": {
        "id": 224,
        "created_at": "2022-11-18T03:52:04.333309Z",
        "updated_at": "2022-11-18T03:52:04.333309Z",
        "text": "전처리.",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_002_전처리.",
        "sequence": 2,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_002_전처리..mp3",
        "tts_project": 2
    },
    "2": {
        "id": 225,
        "created_at": "2022-11-18T03:52:04.707297Z",
        "updated_at": "2022-11-18T03:52:04.707297Z",
        "text": "하실수있도록.",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_003_하실수있도록.",
        "sequence": 3,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_003_하실수있도록..mp3",
        "tts_project": 2
    },
    "3": {
        "id": 226,
        "created_at": "2022-11-18T03:52:05.110018Z",
        "updated_at": "2022-11-18T03:52:05.110018Z",
        "text": "새롭게?",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_004_새롭게？",
        "sequence": 4,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_004_새롭게？.mp3",
        "tts_project": 2
    },
    "4": {
        "id": 227,
        "created_at": "2022-11-18T03:52:05.412570Z",
        "updated_at": "2022-11-18T03:52:05.412570Z",
        "text": "삽입된 문장입니다!",
        "slow": false,
        "name": "GTTS_그냥 프로젝트_005_삽입된 문장입니다!",
        "sequence": 5,
        "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_005_삽입된 문장입니다!.mp3",
        "tts_project": 2
    }
}
```
삽입시킬 문장과 위치를 입력하면 이를 자동으로 전처리해서 프로젝트 내 해당 sequence부터 삽입해줍니다.

![image](https://user-images.githubusercontent.com/101803254/202613419-14bf5a3e-83c1-4e18-8613-04ae084a070f.png)

파일명에도 동일하게 반영됩니다.




## /project/audio/update/ (PUT) (Owner Check: 소유자를 검사합니다.)

### Request
 ```json
{
    "project_title": "그냥 프로젝트",
    "sentense":"업데이트된 2번 문장입니다.",
    "sequence":2
}
 ```
   
### Response
    
 ```json
{
    "id": 224,
    "created_at": "2022-11-18T03:52:04.333309Z",
    "updated_at": "2022-11-18T04:05:44.437937Z",
    "text": "업데이트된 2번 문장입니다.",
    "slow": false,
    "name": "GTTS_그냥 프로젝트_002_업데이트된 2번 문장입니다.",
    "sequence": 2,
    "path": "audio_outputs/그냥 프로젝트/GTTS_그냥 프로젝트_002_업데이트된 2번 문장입니다..mp3",
    "tts_project": 2
}
```
파일명에도 동일 반영됩니다. DB에는 반영하되 기존 파일을 삭제하지는 않습니다.

![image](https://user-images.githubusercontent.com/101803254/202614710-cdcf690d-af07-41f0-87f1-f4fb3e15f810.png)

## /project/ (DELETE) (Owner Check: 소유자를 검사합니다.)

### Request
 ```json
{
    "project_title":"그냥 프로젝트",
    "sequence":2
}
 ```
   
## Response
    
 ```json
"그냥 프로젝트_2delete completed."
```
    
## /project/audio/delete (DELETE) (Owner Check: 소유자를 검사합니다.)

### Request
 ```json
 {
    "project_title":"그냥 프로젝트"
}
 ```
   
### Response
    
 ```json
  "delete complete"
```
    
## 프로젝트 후기

(TODO : 후기 블로그 링크 달기)

차후 고도화한다면, 테스트 커버리지를 더 높이는 방법과 DB hit 수를 줄이도록 쿼리를 더 최적화 하는 방법, 파일 관리에 있어서 삭제, 수정시 기존 파일을 휴지통으로 보내는 기능을 만들고싶습니다. 
