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
- **deploy** : docker, docker-compose

</br>

#### 개발 기간
## - 2023-04-13 ~ 2023-04-16


#### 📰 모델링
![2023-04-16 23 07 05](https://user-images.githubusercontent.com/101803254/232318778-37af0ce9-e0a7-4c2c-8a27-9b886161d862.png)
</br>

#### 🛠 API Test

- 2023-04-16 현재 repo 단 테스트 완료되었습니다.
![image](https://user-images.githubusercontent.com/101803254/232319093-18f01685-3886-4b40-8f8a-a8109b252122.png)

확인방법:
```
cd cafe_service
pytest --cov
```

</br>

## 프로젝트 분석
![제목 없는 다이어그램](https://user-images.githubusercontent.com/101803254/202605476-ae90f7da-6548-4582-b99b-4dbdb975fdb3.jpg)

- DB와 직결되는 모델이 실제 비즈니스 레이어, View 까지 넘어가지 않고 중간에 직렬화를 한번 거치게 함으로써 DB와 모델의 무결성을 보장하였습니다.
- 기존 MVC 패턴에서 너무 한쪽이 비대하지고 책임이 불분명해지는걸 막기위해 클래스들을 나누고 추상클래스, 상속 등을 통해 의존성과 결합도를 낮추고 차후 단위 테스트를 용이하게 하였습니다.

</br>

## 실행방법 & 한번 확인해주세요!

### Config_example.yml
실제 파일은 config.yml 입니다.
로컬에서 실행시 db host 변경해주세요.
```yml
databases:
  host: "db"
  port: 3306
  database: "cafe_service"
  username: "root"
  password: "test1234"
  timezone: "+09:00"

secrets:
  django: "key please"

token:
  scret: "jwt secret"
  referesh_expire_day: 7
  expire_sec: 3600

#한번에 조회할 페이지 수는 설정 파일에 상수로 남겨두었습니다.
page_size:
  page_size: 10
```


### 실행 방법 (로컬)
> ```
>pip install -r requirements.txt
>python manage.py makemigrations
>python manage.py migrate
>python manage.py runserver
>```

### 실행 방법 (docker-compose)
> ```
>cd cafe_service
>docker-compose up -d
>```
## API ENDPOINT
![image](https://user-images.githubusercontent.com/101803254/232319502-9fb915e0-df88-4e65-97e5-0e45c1bdc043.png)
본 프로젝트는 스웨거로 자동 문서화되어있습니다.
http://localhost:8000/swagger/ 에서 확인 가능합니다.

### user

URL|Method|Description|
|------|---|---|
|"signup/"|POST|회원가입|
|"login/"|POST|로그인 : access Token 이 반환되며 헤더에 추가해야 하위 기능들을 이용하실 수 있습니다.|

    
## 프로젝트 후기


