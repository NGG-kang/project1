# 간단한 게시판 프로젝트

- [간단한 게시판 프로젝트](#간단한-게시판-프로젝트)
    - [프로젝트 구성](#프로젝트-구성)
    - [프로젝트 설명](#프로젝트-설명)
    - [프로젝트 설치](#프로젝트-설치)
    - [프로젝트 사용법](#프로젝트-사용법)
    - [프로젝트 기능 설명](#프로젝트-기능-설명)
    - [프로젝트간 애로사항](#프로젝트간-애로사항)
    - [이미지](#이미지)
    - [버그](#버그)
    - [참고 내용](#참고-내용)




[TOC]

## 프로젝트 구성

언어 : `python`, `html`, `css`

프레임워크 : `django`

Database : `sqlite3`(dev) | `mysql`(prod)

라이브러리 : `requirements` 폴더 참조

<br>

## 프로젝트 설명 및 주의사항

`django`를 기반으로 짧게나마 공부 했던 내용을 **게시판** 개념으로 만들어가면서 이해하기 위해 만든 프로젝트 입니다

만들면서 생각나는대로 기능을 추가한 프로젝트라 난잡하게 짜여진 코드입니다

<br>

`dev`와 `prod`로 나눠서 만들었으며

`prod`기반 코드는 `docker`로 `aws`의 `ec2`에 배포하였고 `DB`는 `ec2`에 `mysql`을 설치하여 테스트를 했습니다

static이나 파일 업로드는 `aws S3`를 사용했습니다

<br>

**prod 배포**

주소 : [52.79.235.172:8000](http://52.79.235.172:8000)

단 비용 문제상 `ec2`를 삭제하거나 수정, 배포하는 과정에서 주소가 바뀔 수 있습니다

이미지 참조는 하단의 이미지 구간으로 넘어가면 볼 수 있습니다

<br>

## 프로젝트 설치[dev]

프로젝트 기본 설치

```
$ pip install -r requirements.txt
```

<br>

## 프로젝트 사용법

`dev` 전용 프로젝트 실행

```
$ python manage.py runserver
```



`127.0.0.1:8000`접속


<br>


## 프로젝트 기능 설명

### accounts app

- #### create

  **signup:** 간단한 회원가입 기능 아이디, 이름, 이메일, 패스워드 입력만으로 가입 가능

  **follows:**다른 유저 팔로우 기능

  
<br>


- #### read

  **profile:** 유저 생성시 프로파일 자동 생성, 프로파일 이미지와 상태메시지를 보여준다, 기본값 empty
  				 유저가 생성한 게시글 리스트`post_list`도 같이 보여줌

  **follow_recommend:** 팔로우 유저 추천 기능, 팔로우가 안된 유저들 전부를 불러온다

  **follower_list:**팔로우 된 유저들 리스트

  <br>

- #### update

  **profile_edit:** 프로파일 이미지와 상태메시지를 보여준다

  **comment_edit:** 댓글 수정

  <br>

- #### delete

  **unfollow:**기존 팔로우 유저 팔로우 취소

  <br>

- ### 기타

  **login:**로그인

  **logout:**로그아웃

  
<br>


### nboard app

- #### create

  **post_create:**게시글 생성 기능

  **post_like:**게시글 좋아요 기능

  <br>

- #### read

  **post_detail:**작성된 게시글 상세보기

  <br>

- #### update

  **post_update:**게시글 수정

  <br>

- #### delete

  **comment_delete:**댓글 삭제

  **post_delete:**게시글 삭제

  **post_unlike:** 게시글 좋아요 취소


<br>



## 프로젝트간 애로사항

1. **오로지 django로만 구현하도록 노력했다**
   
   프로젝트의 취지가 오로지 django로만 구현하고 다른 외부 기능들을 최소화 하는것이 나의 목적이었다

   그러나 화면을 구성함에 있어서 `javascript`를 사용하지 않으니 가능한 일이 매우 적다는 문제점
   
   부트스트랩으로 어느정도 꾸몄으나 그래도 화면이 예쁘게 잘 나오지 않는다

<br>   

2. **다른 앱의 view에서 model을 불러오는 문제**
   `from ..nboard.models import Post`로 불러왔더니 불가능
   `from nobard.models import Post`로 불러와도 불가능

   결국 한참을 찾아 알아낸 해결 방법
   `pycharm`에서 `board`를 루트 디렉토리로 넣으니까
   `from nobard.models import Post`로 불러와진다

<br>   

3. **accounts의 커스텀 user과 Profile 자동 생성 문제**

   다른 2가지의 라이브러리를 사용했지만 둘 다 실패
   최근 수정일이 3개월 전이길래 당연히 되는줄 알았지만
   작동이 안되어서 내 문제인줄 알고 프로젝트를 날리고 다시 `model`쪽을 만지작거렸다
   결국 라이브러리 문제라는걸 깨닫고 새로운 라이브러리를 찾아서 해결

   `django_auto_one_to_one`라이브러리를 사용하여 profile 자동으로 생성하도록 하였다

   물론 코드를 보니까 `signal`을 사용해서 뭐 어떻게 하는것 같은데... 나중에 알아보도록 하자

<br>   

4. **민감한 템플릿 코드 문제**

   템플릿 코드 띄어쓰기 문제
   줄바꿈을 안했더니 `include`를 그냥 코드로 반환하는 증상
   그리고 탬플릿 코드 띄어쓰기 실수 했더니 바로 에러가 발생함
   탬플릿 코드는 아주 민감해서 주의해줘야 할 내용인걸 알았다

<br>   

5. **model을 설계를 하지 않고 기능 생각나는대로 추가 했더니 꼬이는 문제**

   프로젝트를 진행하는 과정이 연습삼아 게시판 개념으로 만드는거라

   생각나는대로 기능을 추가하다보니 `model`을 수정하는 일이 잦았다

   그러다 보니 `migrations` 파일도 쌓이고, `view`에 적용하는데 있어서 수정이 잦았다

   다음번엔 모델 설계를 하고 진행을 해 봐야겠다

<br>   


5. **다양한 탬플릿 코드들이 존재하는데 그걸 사용하면 유용하게 쓰일 수 있다는 점**
   `textarea` 자동 줄바꿈이 적용이 가능하다는 점
   `humanize`의 `naturaltime`를 사용하면, 시간의 계산이 없어도 자동으로 몇분 전인지 알려준다

<br>   

6. **커스텀 탬플릿태그를 이용하여 필터를 적용 할 수 있다는 점**

   커스텀 템플릿 태그를 사용하여 return값들을 커스텀하여 돌려줄수 있다는 점이 새로웠다
   단 `view`에서 사용되지 않고, `model`과 `template`에서 사용된다는 점

<br>   

7. **aws 연동 과정에서의 애로사항**

   - **docker**

     `docker`로 리눅스를 설치하여 `ec2`에서 `docker --pulbic`으로 pull하여 docker로 실행했는데....
     그러나 이미 `ec2`는 리눅스로 돌아가는데 `docker`로 또 리눅스 기반으로 돌린다?
     다 만들었는데 리눅스 안에 docker로 리눅스를 돌려버렸다...
     다음 프로젝트는 `python airplane`으로 `docker`를 짜서 하던지
     `aws elastic Beanstalk` 으로 docker 배포가 가능하다고 하니 그 기능을 써봐야겠다

<br>

   - **static, media**

     다음으로S3로 `static`, `media` 저장 과정에서 `버킷 정책` 지정과 `CORS`구성문제...
     검색해서 정책이나 cors구성은 복붙으로 구성하기는 했으나... 잠깐 본 정책으로는 그렇게 어렵게 구성되어 있지는 않았다. 나중에 커스텀으로 할 일이 있다면 보는것도 나쁘지 않을듯

     그 외에도 `media`파일 저장에 있어서 중복이름 파일은 `overwrite`하는 문제가 있었으나
     `django-storages` 설정에 `AWS_S3_FILE_OVERWRITE = False`라는게 있어서 적용해보니
     `django`딴에서 중복 파일들 `rename` 해주는 기능이 잘 작동하는걸 알았다

  <br> 

   - **database**

     `ec2`에 `mysql`을 설치해서 localhost가 아닌 다시 퍼블릭 주소로 데이터베이스 교환하도록 구현했다
     (왜냐하면 localhost로 돌리는 방법을 모르기때문...  아마 docker 리눅스 기반으로 해서 그런듯하다)

     데이터베이스 연결까지는 문제가 없었는데

     그러나 DB encoding문제가 발생
     데이터베이스 설정에 utf8, settings의 database option에도 utf8을 줬으나 그래도 여전히 인코딩에러
     데이터베이스 삭제, 재생성 하니 성공!

 <br>    
 <br>

## 이미지

1. 맨 처음 들어가면 보이는 로그인 화면

   ![login](https://user-images.githubusercontent.com/77260277/115133316-2d1b9480-a042-11eb-98b7-9b6722f0b4f8.PNG)

   <br>

2. 회원가입

   ![signup](https://user-images.githubusercontent.com/77260277/115133320-2e4cc180-a042-11eb-9302-881b653af218.PNG)

   <br>

3. 로그인 하면 `profile`페이지로 이동, 게시글이랑 프로필은 예시

   <img src="https://user-images.githubusercontent.com/77260277/115133318-2db42b00-a042-11eb-9692-90d738e660bc.PNG" alt="profile" style="zoom:50%;" />

   <br>

4. 프로필 수정

   ![profile_edit](https://user-images.githubusercontent.com/77260277/115133319-2db42b00-a042-11eb-8b09-f8bcb231b4da.PNG)

   <br>

5. 팔로워 추천

   ![follow_recommend](https://user-images.githubusercontent.com/77260277/115133314-2c82fe00-a042-11eb-9f0d-5633b8cbe3c3.PNG)

   <br>

6. 팔로잉 리스트

   ![following_list](https://user-images.githubusercontent.com/77260277/115133315-2c82fe00-a042-11eb-832f-20030231c222.PNG)

   <br>

7. 게시글 디테일

   <img src="https://user-images.githubusercontent.com/77260277/115133311-2ab93a80-a042-11eb-92ee-ad223c15d25b.PNG" alt="board_detail" style="zoom:50%;" />

   <br>

8. 게시글 수정

   ![post_edit](https://user-images.githubusercontent.com/77260277/115133317-2d1b9480-a042-11eb-9938-66ac54fdee99.PNG)

   <br>

9. 코멘트 및 수정

   수정을 누르면 하단 코멘트 form에 수정할 내용이 추가됨

   ![comment_and_edit](https://user-images.githubusercontent.com/77260277/115133312-2bea6780-a042-11eb-9012-1a9a132830fa.PNG)


<br>

## 버그 또는 미해결 문제

**팔로우 문제**

팔로우 manytomany로 self user로 연결했는데 
예를 들어 1번과 2번 유저가 있다면, 
1번 유저가 2번 유저를 팔로우 할 시 2번 유저도 1번 유저가 팔로우 되는 증상이 있다
아마 manytomany로 구성해서 그런것 같은데... 
model을 구성하는데 있어서 있는대로 구성하다보니 발생한 문제같다

<br>

**이미지 리사이징 문제**

게시판 형태로 만들다보니 이미지 크기가 안맞으면 이미지가 찌그러지는 현상...
다른 이미지 리사이징 코드를 몇가지 넣어봤지만 리사이징이 안된다 :(

<br>

## 참고 내용

aws S3 연결

https://blog.myungseokang.dev/posts/django-use-s3/

https://ssungkang.tistory.com/entry/Django-AWS-S3%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C

ec2 mysql 서버 연결

https://luji.tistory.com/7

https://nesoy.github.io/articles/2017-05/mysql-UTF8
