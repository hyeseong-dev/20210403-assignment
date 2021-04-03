
# 구현한 API 🚄

- 진행기간 : 2021년 04월 02일 ~ 2021년 04월 03일


## **🏠Swagger **
링크 - https://documenter.getpostman.com/view/14042841/TzCP8Tc4

[사진0]
![image](https://user-images.githubusercontent.com/57933835/113472103-a7251880-949b-11eb-955e-320246f15edc.png)
![image](https://user-images.githubusercontent.com/57933835/113472401-fa986600-949d-11eb-88e3-529e3f8fef74.png)

[사진1]
![image](https://user-images.githubusercontent.com/57933835/113471999-13ebe300-949b-11eb-95cf-cbe6d325d563.png)

[사진2]
![image](https://user-images.githubusercontent.com/57933835/113472039-43025480-949b-11eb-8b2f-4026fd130451.png)

[사진3]
![image](https://user-images.githubusercontent.com/57933835/113472076-88bf1d00-949b-11eb-8ea0-10916c6a92b5.png)

[사진4]
![image](https://user-images.githubusercontent.com/57933835/113471960-e4d57180-949a-11eb-9cd4-b173504d46fb.png)



## **🏠** 

> git clone https://github.com/hyeseong-dev/20210403-assignment.git
> pip install -r requirements.txt
> 




## **🌹기술 스택🌹**
- vscode 1.53.2
- django 3.1.7
- django-extensions 3.1.1
- postman 7.36
- postgresql 12.6
- python 3.8.5


---

# ⭐️ **테이블**
person
환자에 대한 정보를 담고 있습니다.
● person_id : 환자 id
● gender_concept_id : 성별
● birth_datetime : 생년월일
● race_concept_id : 인종
● ethnicity_concept_id : 민족

visit_occurrence
방문에 대한 정보를 담고 있습니다.
● visit_occurrence_id : 방문 id
● person_id : 환자 id
● visit_concept_id : 방문 유형
○ 9201 : Inpatient Visit (입원)
○ 9202 : Outpatient Visit (외래)
○ 9203 : Emergency Room Visit (응급)
● visit_start_datetime : 방문 시작 일시
● visit_end_datetime : 방문 종료 일시

condition_occurrence
진단(병명)에 대한 정보를 담고 있습니다.
● person_id : 환자 id
● condition_concept_id : 진단(병명)
● condition_start_datetime : 진단 시작 일시
● 'condition_end_datetime : 진단 종료 일시
● visit_occurrence_id : 방문 id

drug_exposure
의약품 처방에 대한 정보를 담고 있습니다.
● person_id : 환자 id
● drug_concept_id : 처방 의약품
● drug_exposure_start_datetime : 처방 시작 일시
● drug_exposure_end_datetime : 처방 종료 일시
● visit_occurrence_id : 방문 id

concept
여러 테이블에서 사용되는 concept들의 정보를 담고 있습니다.
● concept_id : concept id
● concept_name : concept 이름
● domain_id : concept가 주로 사용되는 도메인(카테고리)

death
환자의 사망 정보를 담고 있습니다.
● person_id : 환자 id
● death_date : 사망일

## 🌱 Backend


### 1. 환자에 관한 통계 API
● 환자
  ○ 전체 환자 수
  ○ 성별 환자 수
  ○ 인종별 환자 수
  ○ 민족별 환자 수
  ○ 사망 환자 수

### 2. 방문객들에 대한 통계 API
● 방문
  ○ 방문 유형(입원/외래/응급)별 방문 수
  ○ 성별 방문 수
  ○ 인종별 방문 수
  ○ 민족별 방문 수
  ○ 방문시 연령대(10세 단위)별 방문 수

### 3.각 테이블에 사용된 concept_id들의 정보를 얻을 수 있는 API

● 검색 기능
  ○ 키워드 검색
● Pagination 기능

### 4. 각 테이블의 row를 조회하는 API

● concept id와 concept name 매칭
  ○ concept의 의미를 알 수 있게 이름을 함께 return합니다.
● Pagination 기능
● 특정 컬럼 검색 기능
  ○ 키워드 검색

---

# 🏠후기

## 🧑‍💻연락

- 기술 블로그 : https://velog.io/@hyeseong-dev/
- 모바일     : 01058974859
- 이메일     : hyeseong43@gmail.com  



# **레퍼런스**

- 이 프로젝트는 면접 과제를 위한 증명 목적으로 만들었습니다.
- 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제가 될 수 있습니다.
- 이외 다른 문의 사항이 있으시면 
