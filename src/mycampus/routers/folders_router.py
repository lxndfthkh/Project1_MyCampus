from fastapi import APIRouter, Request
#APIRouter : FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#Request : HTTP 요청 정보를 담고 있는 객체
import os 
# os : 운영체제와 상호작용하기 위한 모듈

router = APIRouter(prefix = "/folders", tags = ["folders"])
#APIRouter: FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#prefix = "/folders" : router 안에 정의된 모든 엔드포인트 앞에는 "/folders"가 붙는다
#tags = ["folders"] : swagger ui에서 API들이 folders라는 그룹으로 묶여서 표시됨

base = "uploads"
#base = "uploads" : 폴더들이 저장될 기본 경로


#폴더 만들기 함수
def create_folder(request: Request):
    folder_name = request.query_params.get("folder_name")
    #query_params : 쿼리 매개변수에 접근하기 위한 속성
    path = os.path.join(base, folder_name)
    #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수
    os.makedirs(path, exist_ok=True)
    #os.makedirs : 지정된 경로에 디렉토리를 생성하는 함수
    #exist_ok=True : 이미 디렉토리가 존재해도 에러를 발생시키지 않음
    return {"message": f"Folder '{folder_name}' created successfully."}
    #폴더 생성 성공 메시지 반환

#함수 등록
router.add_api_route(
    path = "/create",
    #요청 주소
    endpoint = create_folder,
    #실행할 함수
    methods = ["GET"],
    #HTTP 메소드
    summary = "create folder"
    #swagger ui에 표시될 이름
    )   