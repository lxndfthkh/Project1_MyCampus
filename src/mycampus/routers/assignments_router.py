from fastapi import APIRouter, Query
#APIRouter : FastAPI에서 라우터 객체를 만들고 특정 기능을 묶는 클래스
#Query : 쿼리 파라미터를 처리하기 위한 클래스
from typing import Optional
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
    def __init__(self, course_name: str, week: str, title: str, due_date: str):
        self.course_name = course_name
        self.week = week
        self.title = title
        self.due_date = due_date
    
    def save(self):

        folder_path = os.path.join(base, self.course_name, self.week)
        #os.path.join : 여러 경로를 하나의 경로로 조합하는 함수

        os.makedirs(folder_path, exist_ok=True)
        #os.makedirs : 지정된 경로에 디렉토리를 생성하는 함수
        #exist_ok=True : 이미 디렉토리가 존재해도 에러를 발생시키지 않음

        file_path = os.path.join(folder_path, "assignments.txt")
        with open (file_path, "a", encoding = "utf-8") as f:
            f.write(f"{self.title} | {self.due_date}\n")
        return file_path


#과제 만들기 함수
def create_assignment(course_name : str = Query(..., description = "Name of the course (ex: webpython)"),
                      week : str = Query(..., description = "Week Number (ex: 01)"),
                      title : str = Query (..., description = "Assignment Title (ex: 'Assignment1')"),
                      due_date : str = Query (..., description = "Due Date (ex: 20251130)")):
    # Course : str = Query(...) : 쿼리 파라미터로 Course 값을 받음
    # Week : str = Query(...) : 쿼리 파라미터로 Week 값을 받음
    # Title : str = Query(...) : 쿼리 파라미터로 Title
    # Due_date : str = Query(...) : 쿼리 파라미터로 Due_date 값을 받음
    assignment = Assignment(course_name, week, title, due_date)
    file_path = assignment.save()
    return {"message": f"Assignment saved to {file_path}"}
    #과제 저장 성공 메시지 반환

#과제 읽기 함수
def read_assignment(file_path: str):
    if not os.path.exists(file_path):
        return {
            "file" : file_path,
            "assignments" : 0,
            "specification" : [],
            "message" : f"File '{file_path}' does not exist."
        }
    
    specification = []

    with open (file_path, "r", encoding = "utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 2:
                title, due_date = parts
            else:
                title, due_date = parts[0], "N/A"
            specification.append({
                "title" : title.strip(),
                "due_date" : due_date.strip()
            })
    return {
        "file" : file_path,
        "assignments" : len(specification),
        "specification" : specification
    }

#과제 목록 함수
def list_assignments(course_name : str = Query(..., description = "Name of the course (ex: webpython)"),
                     week : str | None = Query(None, description = "Week Number (ex: 01)")):
    course_path = os.path.join(base, course_name)

    if not os.path.exists(course_path):
        return{
            "course" : course_name,
            "assignments" : [],
            "specification" : f"course folder '{course_path}' does not exist."
        }
    
    all_specification = []

    if week:
        file_path = os.path.join(course_path, week, "assignments.txt")
        result = read_assignment(file_path)
        return{
            "course" : course_name,
            "week" : week,
            "assignments" : result["assignments"],
            "specification" : result["specification"]
        }
    for dir_name in sorted(os.listdir(course_path)):
        week_path = os.path.join(course_path, dir_name)
        if not os.path.isdir(week_path):
            continue
        file_path = os.path.join(week_path, "assignments.txt")
        if not os.path.exists(file_path):
            continue
    
        result = read_assignment(file_path)

        for assignment in result["specification"]:
            all_specification.append({
            "week" : dir_name,
            "title" : assignment["title"],
            "due_date" : assignment["due_date"]
        })
    return{
    "course" : course_name,
    "assignments" : len(all_specification),
    "specification" : all_specification
}

#과제 삭제 함수
def delete_assignment(course_name : str = Query(..., description = "Name of the course (ex: webpython)"),
                      week : str = Query(..., description = "Week Number (ex: 01)"),
                      title : str = Query (..., description = "Assignment Title (ex: 'Assignment1')")):
    file_path = os.path.join(base,course_name, week, "assignments.txt")

    if not os.path.exists(file_path):
        return {"message": f"Assignment file '{file_path}' not found."}
    
    lines = []
    deleted = False

    with open (file_path, "r", encoding = "utf-8") as f:
        for line in f:
            if  not line.strip().startswith(f"{title} |"):
                lines.append(line)
            else:
                deleted = True
    
    with open(file_path, "w", encoding = "utf-8") as f:
        f.writelines(lines)
    if deleted:
        return {"message": f"Assignment '{title}' deleted successfully."}
    else:
        return {"message" :f"Assignment '{title}' not found in {file_path}"}

def update_status(course_name : str = Query(..., description = "Name of the course (ex: webpython)"),
                        week : str = Query(..., description = "Week Number (ex: 01)"),
                        title : str = Query (..., description = "Assignment Title (ex: 'Assignment1')"),
                        status : str = Query(..., description = "Current Status (ex: In progress, Completed)"),
                        end_date : str = Query(..., description = "End Date (ex: 20251203)"),
                        note :Optional[str] = Query (None, description = "")):
    file_path = os.path.join(base, course_name, week, "assignments.txt")
    if not os.path.exists(file_path):
        return {"message": f"Assignment file '{file_path}' not found."}
    
    updated = False
    lines = []

    with open (file_path, "r", encoding = "utf-8") as f:
        for line in f:
            content = line.strip()
            if not content:
                continue
            parts = [p.strip() for p in content.split("|")]
            if len(parts) >= 2 and parts[0] == title:
                old_title = parts[0]
                old_due_date = parts[1]
                while len(parts) < 5:
                    parts.append("")
                parts[2] = status
                parts[3] = end_date
                if note is not None:
                    parts[4] = note
                new_line = " | ".join([old_title, old_due_date,parts[2], parts[3], parts[4]]+'\n')
                lines.append(new_line)
                updated = True
            else:
                lines.append(line)
    
    if not updated:
        return {"message": f"Assignment {title} not found in {file_path}."}
    
    with open(file_path, "w", encoding = "utf-8") as f:
        f.writelines(lines)
    return{
        "message" : "Assignment status updated",
        "course" : course_name,
        "week" : week,
        "title" : title,
        "status": status,
        "end_date" : end_date,
        "note" : note,
        "path" : file_path
    }
                

                

            
#함수 등록
router.add_api_route(
    path = "/create", #요청 주소
    endpoint = create_assignment, #실행할 함수
    methods = ["POST"], #HTTP 메소드
    summary = "create assignment" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/list", #요청 주소
    endpoint = list_assignments, #실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "list assignments" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/delete", #요청 주소
    endpoint = delete_assignment, #실행할 함수
    methods = ["DELETE"], #HTTP 메소드
    summary = "delete assignment" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/status", #요청 주소
    endpoint = update_status, #실행할 함수
    methods = ["PUT"], #HTTP 메소드
    summary = "Update assignment status" #swagger ui에 표시될 이름
)