from fastapi import APIRouter, Query
#APIRouter : FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#Query : 쿼리 파라미터를 처리하기 위한 클래스
import os 
# os : 운영체제와 상호작용하기 위한 모듈

router  = APIRouter(prefix = "/assignments", tags = ["assignments"])
#APIRouter: FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#prefix = "/assignments" : router 안에 정의된 모든 엔드포인트 앞에는 "/assignments"가 붙는다
#tags = ["assignments"] : swagger ui에서 API들이 assignments라는 그룹으로 묶여서 표시됨

base = "storage"
#base = "storage" : 과제 폴더들이 저장될 기본 경로

#과제 클래스
class Assignment:
    def __init__(self, course: str, week: str, title: str, due_date: str):
        self.course = course
        self.week = week
        self.title = title
        self.due_date = due_date
    
    def save(self):

        folder_path = os.path.join(base, self.course, self.week)
        #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수

        os.makedirs(folder_path, exist_ok=True)
        #os.makedirs : 지정된 경로에 디렉토리를 생성하는 함수
        #exist_ok=True : 이미 디렉토리가 존재해도 에러를 발생시키지 않음

        file_path = os.path.join(folder_path, "assignments.txt")
        with open (file_path, "a", encoding = "utf-8") as f:
            f.write(f"{self.title} | {self.due_date}\n")
        return file_path


#과제 만들기 함수
def create_assignment(course : str = Query(..., description = "Name of the course (ex: webpython)"),
                      week : str = Query(..., description = "Week Number (ex: 01)"),
                      title : str = Query (..., description = "Assignment Title (ex: 'Assignment1')"),
                      due_date : str = Query (..., description = "Due Date (ex: 20251130)")):
    # Course : str = Query(...) : 쿼리 파라미터로 Course 값을 받음
    # Week : str = Query(...) : 쿼리 파라미터로 Week 값을 받음
    # Title : str = Query(...) : 쿼리 파라미터로 Title
    # Due_date : str = Query(...) : 쿼리 파라미터로 Due_date 값을 받음
    assignment = Assignment(course, week, title, due_date)
    file_path = assignment.save()
    return {"message": f"Assignment saved to {file_path}"}
    #과제 저장 성공 메시지 반환

def read_assignment(file_path: str):
    if not os.path.exists(file_path):
        return {"message": f"File '{file_path}' does not exist."}
    
    parts = []
    with open (file_path, "r", encoding = "utf-8") as f:
        content = f.read()
        parts = content.splitlines()
    return parts


#함수 등록
router.add_api_route(
    path = "/create", #요청 주소
    endpoint = create_assignment, #실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "create assignment" #swagger ui에 표시될 이름
)