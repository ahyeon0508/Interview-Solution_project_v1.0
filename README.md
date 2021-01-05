# 숭실대학교 소프트웨어학부 캡스톤디자인종합프로젝트

## 프로젝트명
- 새내기路(로) : AI기반 대입 모의 면접 솔루션

-----------------

### 1. 프로젝트의 개요
#### 1-1. 프로젝트 개발 배경
&nbsp;&nbsp;&nbsp;현재 대한민국의 대학 입시 제도에는 수시모집전형(학생부종합전형, 학생부교과전형 등), 정시모집전형 등 다양한 전형이 존재한다. 대다수의 대학들이 면접전형을 시행하고 있으며, 대학별 반영비율에 따라 최종합격의 당락을 좌우한다. 이에 대해 대입 수험생들은 면접전형에 부담감을 느끼고 있다.  
&nbsp;&nbsp;&nbsp;면접에 부담감을 느끼는 사람들을 대상으로 인공지능(artificial intelligence, 이하 AI) 모의 면접 서비스가 제공되고 있지만, 대부분 취업 준비생들을 대상으로 하고 있어 대입 수험생들을 위한 서비스는 부족한 실정이다.  
&nbsp;&nbsp;&nbsp;따라서 본 프로젝트의 목적은 대입 수험생들에게 AI 기술을 기반으로 하여 모의 면접 서비스를 제공하는 것이다. 이 서비스는 면접 시 사용자의 답변 내용과 태도를 분석하여 결과를 제공함으로써 면접 상황에서의 본인의 모습을 파악하고 면접능력을 개발하도록 도와준다.  

#### 1-2. 프로젝트 목표 및 주요 기능
#### 최종 목표 : AI 기술을 이용한 대입 면접 수험생용 모의 면접 및 면접 결과 분석 서비스 개발

#### 주요 기능
| 기능 | 역할 |
| ------ | ------ |
| 질문 | 모의 면접에 사용할 질문들을 제공 및 관리하는 기능 <br> - 미리 제공되는 질문 : 공통 질문, 학과별 질문 <br> - 사용자가 입력하는 질문 : 사용자 작성 질문, 교사에게 공유 받은 질문|
| 면접 기록 | 질문별 영상 녹화 기능 및 답변 내용을 대본으로 기록하는 기능 |
| 면접 분석 | - 답변 분석 : 답변 내용에서 감탄사(음, 어)와 반복어 빈도를 계산하여 보여주는 기능<br> - 태도 분석 : 말하기 속도를 분석하는 기능 |
| 공유 | 교사에게 영상 및 질문을 공유할 수 있는 기능 |

### 2. 개발 환경 및 개발 언어
|| tool |
| ------ | ------ |
| 개발언어 | ![issue badge](https://img.shields.io/badge/python-3.7.4-blue.svg) ![issue badge](https://img.shields.io/badge/javascript-blue.svg) |
| 라이브러리 & 프레임워크 | ![issue badge](https://img.shields.io/badge/Django-3.0.3-green.svg) ![issue badge](https://img.shields.io/badge/jQuery-green.svg) ![issue badge](https://img.shields.io/badge/Bootstrap-green.svg) ![issue badge](https://img.shields.io/badge/OpenCV-4.5.0-green.svg) ![issue badge](https://img.shields.io/badge/pyaudio-green.svg) ![issue badge](https://img.shields.io/badge/moviepy-green.svg) |
| Open API | [ETRI 음성 인식 API](https://aiopen.etri.re.kr/guide_recognition.php) [ETRI 형태소 인식 API](https://aiopen.etri.re.kr/guide_wiseNLU.php) [커리어넷 학교 정보 오픈 API](https://www.career.go.kr/cnet/front/openapi/openApiMainCenter.do) |
| 개발환경 | Windows10 |
| 데이터베이스 환경 | ![issue badge](https://img.shields.io/badge/SQL-sqlite-lightgrey.svg) |

### 3. 시스템 구조도

&nbsp;&nbsp;&nbsp;[그림 1]은 본 프로젝트의 구조도이며 캡스톤디자인종합프로젝트1과 캡스톤디자인종합프로젝트2의 개발 내용이 담겨져 있다. 본 repository는 캡스톤디자인종합프로젝트1의 개발 내용로 구성되어 있으며, 캡스톤디자인종합프로젝트2의 개발 내용은 해당 깃허브[Interview-Solution_project_2.0](https://github.com/ahyeon0508/Interview-Solution_project_v2.0)를 참고한다.  
&nbsp;&nbsp;&nbsp;[그림 2]는 ER diagram이다.

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658975-4460d580-4faf-11eb-83ca-863a4e3b8742.png" alt="구조도" width="50%" height="50%"  />
  [그림 1] 시스템 구조도<br>
</p><br><br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103659029-50e52e00-4faf-11eb-97f5-1b9c70062c9c.png" alt="ER diagram" width="50%" height="50%"  />
  [그림 2] ER diagram<br>
</p> 
 

### 4. 새내기路(로) 결과 화면 일부
  
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658978-44f96c00-4faf-11eb-99a2-fb4d30ea463f.png" alt="메인 화면" width="50%" height="50%"  />
  [그림 3] 새내기路(로) 메인 화면 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658966-42971200-4faf-11eb-9082-89f0c1db12a3.png" alt="학생 메인 화면" width="50%" height="50%"  />
  [그림 4] 학생 메인 화면 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658974-43c83f00-4faf-11eb-8409-449dccc56a3e.png" alt="교사 메인 화면" width="50%" height="50%"  />
  [그림 5] 교사 메인 화면 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658976-4460d580-4faf-11eb-866f-2c52cdf1b513.png" alt="내 질문 리스트" width="50%" height="50%"  />
  [그림 6] 내 질문 리스트 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658988-462a9900-4faf-11eb-94dc-63c21da82554.png" alt="면접 질문 설정 화면" width="50%" height="50%"  />
  [그림 7] 면접 질문 설정 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658984-45920280-4faf-11eb-970f-9476ad90ff62.png" alt="면접 세팅 화면" width="50%" height="50%"  />
  [그림 8] 면접 세팅 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658987-462a9900-4faf-11eb-8cad-b6d1a20ed568.png" alt="면접 진행 화면" width="50%" height="50%"  />
  [그림 9] 면접 진행 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658979-44f96c00-4faf-11eb-969a-6736f5b370f6.png" alt="면접 대기 화면" width="50%" height="50%"  />
  [그림 10] 면접 대기 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658980-45920280-4faf-11eb-953f-f79c2515290d.png" alt="면접 리포트 화면" width="50%" height="50%"  />
  [그림 11] 면접 리포트 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658972-43c83f00-4faf-11eb-8383-1675e99fd0be.png" alt="면접 대기 화면" width="50%" height="50%"  />
  [그림 12] 학생 면접 영상 페이지 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/103658991-46c32f80-4faf-11eb-8c61-4e2d626aec78.png" alt="예상 질문 전송 화면" width="50%" height="50%"  />
  [그림 13] 예상 질문 전송 페이지 <br>
</p> <br>


-----------------
## 프로젝트 기간
2020.09 - 2020.12

## Contributor
+ 팀명 : 말하는 감자들
+ 팀장 : 숭실대학교 소프트웨어학부 이아현
+ 팀원 : 숭실대학교 소프트웨어학부 박수현
+ 팀원 : 숭실대학교 소프트웨어학부 진혜원
+ 팀원 : 숭실대학교 소프트웨어학부 채예진

## 수상
2020 ETRI 오픈 API 활용사례 공모전 - 가작 수상