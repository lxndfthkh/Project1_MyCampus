from fastapi import APIRouter, Query
import os 
import shutil


router = APIRouter(prefix = "/courses", tags = ["courses"])

base = "storage"



class Course:
    def __init__(self, name: str, week: str, learning_tool: str):
        self.name = name
        self.week = week
        self.learning_tool = learning_tool


    @property
    def path(self):
        return os.path.join(base, self.name, self.week, self.learning_tool)
    
    @property
    def week_root(self):
        return os.path.join(base, self.name, self.week)

    def create(self):
        os.makedirs(self.path, exist_ok = True)
        return self.path
    
    def delete(self):
        shutil.rmtree(self.path)
        return self.path



#폴더 만들기 함수
def create_course(course_name : str = Query(..., description = "Name of the course (ex: webpython)"),
                  week : str = Query(..., description = "Week Number (ex: 01)"),
                  learning_tool : str = Query(..., description = "Lecturenote, Assignment, Project (ex: 'Lecturenote')")):
    course = Course(course_name, week, learning_tool)
    created_path = course.create() 
    return {"message": "Course created successfully.",
            "path": created_path}

#폴더 삭제 함수
def delete_course(course_name: str = Query(..., description = "Name of the course (ex: webpython)"),
                  week : str = Query(..., description = "Week number (ex: 01)"),
                  learning_tool : str = Query(..., description = "Lecturenote, Assignment, Project (ex: 'Lecturenote')")):
    
    course = Course(course_name, week, learning_tool)
    target_path = course.path

    if not os.path.exists(target_path):
        return {"message": f"Course path '{target_path}' does not exist."}
    
    deleted_path = course.delete()

    return {"message": "Course deleted successfully."}


#함수 등록
router.add_api_route(
    path = "/create", #요청 주소
    endpoint = create_course, #실행할 함수
    methods = ["POST"], #HTTP 메소드
    summary = "create course" #swagger ui에 표시될 이름
    )

router.add_api_route(
    path = "/delete", #요청 주소
    endpoint = delete_course, #실행할 함수
    methods = ["DELETE"], #HTTP 메소드
    summary = "delete course" #swagger ui에 표시될 이름
)