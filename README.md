# sound-compliation

 - # 문장을 TTS 음성이 담긴 mp3 파일로 생성을 하는 역할을 합니다.
 - 기본 저장경로는 ./audio_output 입니다. 
 - 파일 명명규칙은 GTTS_{project_title}_{text}_{sequense}.mp3 입니다.

## DataBase
![tts_project](https://user-images.githubusercontent.com/101803254/201925638-b7648f15-69b8-4ba1-9ac5-4a40eb0c5a90.png)

## 기능

 - 프로젝트 생성(오디오 생성)
    - 텍스트(str)가 담긴 리스트를 받습니다. (length = 1)
    - 이를 전처리하여 오디오를 생성하는 함수의 input으로 같이 넣습니다.
    - [['text1', 'text2', 'text3', ....], path]
    - 일정시간 이후 함수에서 (id, text)형태의 원소를 가진 리스트를 리턴합니다.
    - [('id1' ,'text1'), ('id2', 'text2'), ('id3', 'text3'), ....]
    - 오디오는 input의 path에 저장됩니다.
    
    
## /project/ (POST)

## Request
 ```json
    {
    "project_title": "새로운 대사들",
    "sentenses": "즉, 중첩 딕셔너리는 계층형 데이터를 저장할 때 유용합니다. 딕셔너리 안에 들어있는 딕셔너리에 접근하려면 딕셔너리 뒤에 [ ](대괄호)를 단계만큼 붙이고 키를 지정해주 면 됩니다. 여기서는 딕셔너리가 두 단계로 구성되어 있으므로 대괄호를 두 번 사용합니다.template_name template_name이 제공된 경우, HTML 렌더러 또는 일부 다른 사용자 지정 template렌더러가 response에 승인된 렌더러인 경우에만 필요합니다.accepted_rendererresponse를 렌더링하는 데 사용할 렌더러 인스턴스입니다.response가 view에서 반환되기 직전에 APIView 또는 @api_view에 의해 자동으로 설정됩니다. "}
   ```
   
## Response
    
 ```json
    {
    "1": {
        "id": 45,
        "created_at": "2022-11-15T12:41:14.588955Z",
        "updated_at": "2022-11-15T12:41:14.588955Z",
        "text": "즉, 중첩 딕셔너리는 계층형 데이터를 저장할 때 유용합니다.",
        "slow": 0.0,
        "name": "GTTS_즉, 중첩 딕셔너리는 계층형 데이터를 저장할 때 유용합니다._000",
        "sequense": 0,
        "path": "audio_outputs\\GTTS_새로운 대사들_즉, 중첩 딕셔너리는 계층형 데이터를 저장할 때 유용합니다._000",
        "tts_project": 7
    },
    "2": {
        "id": 46,
        "created_at": "2022-11-15T12:41:14.938015Z",
        "updated_at": "2022-11-15T12:41:14.938015Z",
        "text": "딕셔너리 안에 들어있는 딕셔너리에 접근하려면 딕셔너리 뒤에  대괄호를 단계만큼 붙이고 키를 지정해주면 됩니다.",
        "slow": 0.0,
        "name": "GTTS_딕셔너리 안에 들어있는 딕셔너리에 접근하려면 딕셔너리 뒤에  대괄호를 단계만큼 붙이고 키를 지정해주면 됩니다._001",
        "sequense": 1,
        "path": "audio_outputs\\GTTS_새로운 대사들_딕셔너리 안에 들어있는 딕셔너리에 접근하려면 딕셔너리 뒤에  대괄호를 단계만큼 붙이고 키를 지정해주면 됩니다._001",
        "tts_project": 7
    }, 
    
    ...
    
    "6": {
        "id": 50,
        "created_at": "2022-11-15T12:41:16.799126Z",
        "updated_at": "2022-11-15T12:41:16.799126Z",
        "text": "response가 view에서 반환되기 직전에 APIView 또는 api_view에 의해 자동으로 설정됩니다.",
        "slow": 0.0,
        "name": "GTTS_response가 view에서 반환되기 직전에 APIView 또는 api_view에 의해 자동으로 설정됩니다._005",
        "sequense": 5,
        "path": "audio_outputs\\GTTS_새로운 대사들_response가 view에서 반환되기 직전에 APIView 또는 api_view에 의해 자동으로 설정됩니다._005",
        "tts_project": 7
    },
    "project": {
        "id": 7,
        "created_at": "2022-11-15T12:39:39.116139Z",
        "updated_at": "2022-11-15T12:41:14.232733Z",
        "project_title": "새로운 대사들",
        "user": 1
    }
}
```

![image](https://user-images.githubusercontent.com/101803254/201928330-43470005-f37c-470d-aa09-0356adec6990.png)

    
  - 텍스트 조회
    - 특정 프로젝트의 n번째 페이지를 조회합니다.
    - 한페이지는 10문장으로 이루어져 있습니다.
  - 텍스트 수정
    - 한 문장의 텍스트와 스피드를 수정합니다.
    - 오디오파일 송신
    - 요청받은 오디오파일을 송신합니다.
    - 텍스트(오디오) 생성 / 삭제
    - 삽입위치는 항상 앞, 뒤가 아닌 중간도 가능.
  -프로젝트 삭제
  
  
