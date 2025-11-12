from fastapi import APIRouter, UploadFile, File, Form
#APIRouter : FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#UploadFile : 업로드된 파일을 나타내는 클래스
#File : 파일 업로드를 처리하기 위한 클래스
#Form : HTML form 데이터를 처리하기 위한 클래스
import os
# os : 운영체제와 상호작용하기 위한 모듈

router = APIRouter(prefix = "/files", tags = ["files"])
#APIRouter: FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#prefix = "/files" : router 안에 정의된 모든 엔드포인트 앞에는 "/files"가 붙는다
#tags = ["files"] : swagger ui에서 API들이 files라는 그룹으로 묶여서 표시됨

base = "storage"
#base = "storage" : 파일들이 저장될 기본 경로

os.makedirs(base, exist_ok = True)
#os.makedirs : 지정된 경로에 디렉토리를 생성하는 함수
#exist_ok=True : 이미 디렉토리가 존재해도 에러를 발생시키지 않음

#파일 업로드 함수
def upload_file(file: UploadFile = File(...),
                course : str = Form(...),
                week : str = Form(...),
                learning_tool : str = Form(...)):
    #file: UploadFile = File(...) : FastAPI에서 파일 업로드를 처리하기 위한 구문#
    #Course : str = Form(...) : HTML form 데이터에서 Course 값을 받음
    #Week : str = Form(...) : HTML form 데이터에서 Week 값을 받음
    #Learning_tool : str = Form(...) : HTML form 데이터에서 Learning_tool 값을 받음

    path = os.path.join(base, course, week, learning_tool)
    #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수

    if not os.path.exists(path):
        return {"message" : f"Folder '{path}' does not exist."}
    #os.path.exists : 지정된 경로가 존재하는지 확인하는 함수, 폴더가 없으면 저장하지 않음

    save_path = os.path.join(path, file.filename)
    #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수, 파일이 실제로 저장되는 전체 경로 생성

    with open(save_path,"wb") as uploaded_file:
        uploaded_file.write(file.file.read())
    #"wb" : 쓰기 모드, 이미지, pdf 등 깨짐 방지
    #file.file.read(): 업로드된 파일의 내용을 읽음

    return {"message" : f"{file.filename} saved to {save_path}"}
    #파일 저장 성공 메시지 반환

#파일 삭제 함수
def delete_file(course : str = Form(...),
                week : str = Form(...), 
                learning_tool : str = Form(...),
                filename : str = Form(...)):
    path = os.path.join(base, course, week, learning_tool, filename)
    if not os.path.exists(path):
        return{"message" : f"File '{path}' does not exist."}
    
    os.remove(path)
    #os.remove : 지정된 경로의 파일을 삭제하는 함수

    return{"message" : f"File '{path}' deleted successfully."}

router.add_api_route(
    path = "/upload", #요청 주소
    endpoint = upload_file, #실행할 함수
    methods = ["POST"], #HTTP 메소드
    summary = "upload file" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/delete", #요청 주소
    endpoint = delete_file, #실행할 함수
    methods = ["DELETE"], #HTTP 메소드
    summary = "delete file" #swagger ui에 표시될 이름
)