웹/파이썬 프로그래밍 프로젝트 
2022105698 소광현
GitHub repository
https://github.com/lxndfthkh/Project1_MyCampus.git

**  MyCampus  **
MyCampus는 강의 자료, 과제, 팀 정보를 정리하기 위한 개인 학습 관리 백엔드 서버입니다.
FastAPI를 기반으로 구축되었으며 학습 폴더 및 파일을 체계적으로 관리하고 다양한 기능들을 제공합니다.

이 프로젝트는 FastAPI의 내장 문서화 기능인 Swagger UI를 사용하여 모든 API를 브라우저에서
바로 테스트 할 수 있습니다.

**  목표  **
개인 학습 자료 및 과제를 정리하고 관리할 수 있는 경량형 학습 관리 서버를 구축하는 것이 목표입니다.
여러 기기에서 공통 api로 접근 가능하게 하는 것이 목표이며 간단하고 확장성 높은 구조를 가지고 있습니다.

**  프로젝트 파일 구조 **
MyCampus/
├── pyproject.toml
├── README.md
├── storage/                      # 실제 데이터가 저장되는 폴더 (동적으로 생성)
│
└── src/
    └── mycampus/
        ├── main.py               # FastAPI 메인 서버
        │
        ├── routers/              # 기능별 라우터 폴더
        │   ├── courses_router.py     # 코스 & 폴더 관리
        │   ├── files_router.py       # 파일 업로드/다운로드/삭제/목록
        │   ├── assignments_router.py # 과제 CRUD + 상태 업데이트
        │   └── team_router.py         # 팀 생성 및 정보 조회
        │
        └── __init__.py

**  실행 방법  **
맞는 디렉토리에서 다음을 실행
poetry run uvicorn main:app --app-dir src/mycampus

**  접속 경로  **
http://127.0.0.1:8000      # 홈 화면
http://127.0.0.1:8000/docs # Swagger UI 


**  주요 기능  **
/courses : 코스 기능 및 폴더 관리
파일 - courses_router.py
- 코스 생성
- 주차 생성
- 학습 도구 폴더 생성
- 폴더 삭제

/files : 파일 관리
파일: files_router.py
- 파일 업로드
- 파일 다운로드
- 파일 삭제
- 파일 목록 조회

/assignments: 과제 관리
파일 - assignments_router.py
- 과제 생성
- 특정 주차 과제 조회
- 전체 주차 과제 조회
- 과제 삭제
- 과제 상태 업데이트

/team: 팀 관리
파일 - team_router.py
- 특정 코스 내 팀 생성
- 팀 정보 파일 


**  저장 구조  **
폴더 및 파일의 저장 구조
storage/
 └── course_name/
        └── 01/
             ├── Lecturenote/
             ├── Assignment/
             ├── Project/
             ├── assignments.txt
             └── _teams/
                   └── TeamA/
                       └── team_info.txt

