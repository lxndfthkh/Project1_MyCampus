from fastapi import APIRouter, UploadFile, File, Form, Query
import os
from fastapi.responses import FileResponse

router = APIRouter(prefix = "/files", tags = ["files"])

base = "storage"

os.makedirs(base, exist_ok = True)

#파일 업로드 함수
def upload_file(file: UploadFile = File(...),
                course_name : str = Form(...),
                week : str = Form(...),
                learning_tool : str = Form(...)):
    path = os.path.join(base, course_name, week, learning_tool)


    if not os.path.exists(path):
        return {"message" : f"Folder '{path}' does not exist."}
    

    save_path = os.path.join(path, file.filename)
    
    with open(save_path,"wb") as uploaded_file:
        uploaded_file.write(file.file.read())
    
    return {"message" : f"{file.filename} saved to {save_path}"}
    
#파일 삭제 함수
def delete_file(course_name : str = Form(...),
                week : str = Form(...), 
                learning_tool : str = Form(...),
                filename : str = Form(...)):
    path = os.path.join(base, course_name, week, learning_tool, filename)
    if not os.path.exists(path):
        return{"message" : f"File '{path}' does not exist."}
    
    os.remove(path)
   
    return{"message" : f"File '{path}' deleted successfully."}

#파일 다운로드 함수
def download_file(course_name: str = Query(..., description = "Name of the course (ex: webpython)"),
                  week : str = Query(..., description = "Week number (ex: 01)"),
                  learning_tool : str = Query(..., description = "Lecturenote, Assignment, Project (ex: 'Lecturenote')"),
                  file_name : str = Query(..., description = "File name (ex: Lecturenote1.txt")):
    path = os.path.join(base,course_name, week, learning_tool, file_name)

    if not os.path.exists(path) or not os.path.isfile(path):
        return{"message" : f"File '{path}' does not exist."}
    return FileResponse(
        path,
        media_type = "application/octet-stream",
        filename = file_name
    )
    
#파일 목록 조회 함수

def files_list(course_name:str = Query(...,description = "Name of the course (ex: webpython)"),
               week: str = Query(..., description = "Week number (ex: 01)"),
               learning_tool : str = Query(..., description = "Lecturenote, Assignment, Project (ex: 'Lecturenote')")):
    path = os.path.join(base, course_name, week, learning_tool)
    if not os.path.exists(path) or not os.path.isdir(path):
        return{
            "course": course_name,
            "week": week,
            "learning_tool": learning_tool,
            "files_count": 0,
            "files": [],
            "specification": f"Folder '{path}' does not exist."
        }
    
    items = os.listdir(path)

    files = []
    for item in items:
        if os.path.isfile(os.path.join(path, item)):
            files.append(item)
    
    return{"course": course_name,
           "week": week,
           "learning_tool": learning_tool,
           "files_count": len(files),
           "files": files}


#함수 등록
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

router.add_api_route(
    path = "/list", #요청 주소
    endpoint = files_list, #실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "list files" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/download", #요청 주소
    endpoint = download_file,#실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "download file" #swagger ui에 표시될 이름
    )