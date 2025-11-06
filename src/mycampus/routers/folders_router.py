from fastapi import APIRouter, Query
#APIRouter : FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#Query : 쿼리 파라미터를 처리하기 위한 클래스
import os 
# os : 운영체제와 상호작용하기 위한 모듈

router = APIRouter(prefix = "/folders", tags = ["folders"])
#APIRouter: FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#prefix = "/folders" : router 안에 정의된 모든 엔드포인트 앞에는 "/folders"가 붙는다
#tags = ["folders"] : swagger ui에서 API들이 folders라는 그룹으로 묶여서 표시됨

base = "storage"
#base = "storage" : 폴더들이 저장될 기본 경로


#폴더 만들기 함수
def create_folder(course : str = Query(..., description = "Name of the course (ex: webpython)"),
                  week : str = Query(..., description = "Week Number (ex: 01)"),
                  learning_tool : str = Query(..., description = "Lecturenote, Assignment, Project (ex: 'Lecturenote')")):
    #Course : str = Query(...) : 쿼리 파라미터로 Course 값을 받음
    #Week : str = Query(...) : 쿼리 파라미터로 Week 값을 받음
    #Learning_tool: str = Query(...) : 쿼리 파라미터로 Learning_tool 값을 받음
    path = os.path.join(base, course, week, learning_tool)
    #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수
    os.makedirs(path, exist_ok=True)
    #os.makedirs : 지정된 경로에 디렉토리를 생성하는 함수
    #exist_ok=True : 이미 디렉토리가 존재해도 에러를 발생시키지 않음
    return {"message": f"Folder created successfully."}
    #폴더 생성 성공 메시지 반환

#함수 등록
router.add_api_route(
    path = "/create", #요청 주소
    endpoint = create_folder, #실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "create folder" #swagger ui에 표시될 이름
    )   