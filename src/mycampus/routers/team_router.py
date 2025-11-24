from fastapi import APIRouter, Query
import os

from mycampus.routers.courses_router import base

router = APIRouter(prefix = "/teams", tags = ["teams"])

class Team:
    def __init__ (self, course_name: str, team_name: str):
        self.course_name = course_name
        self.team_name = team_name

    
    @property
    def folder_path(self):
        return os.path.join(base, self.course_name, "_teams", self.team_name)
    
    @property
    def info_file(self):
        return os.path.join(self.folder_path, "team_info.txt")
    
    def create(self):
        os.makedirs(self.folder_path, exist_ok = True)
        return self.folder_path
    


def create_team(course_name: str = Query(..., description = "Name of the course (ex: webpython)"),
                team_name: str = Query(..., description = "Name of the team (ex: Team A)")):
    team = Team(course_name, team_name)
    folder = team.create()

    if os.path.exists(team.info_file):
        return {
            "message": f"Team '{team_name}' already exists in course '{course_name}'.",
            "course": course_name,
            "team": team_name,
            "path": folder
        }

    with open(team.info_file, "w", encoding="utf-8") as f:
        f.write(f"course : {course_name}\n")
        f.write(f"team : {team_name}\n")
    
    return {"message": "Team created successfully.",
            "course": course_name,
            "team": team_name,
            "path": folder}


def get_team(course_name: str = Query(..., description = "Name of the course (ex: webpython)"),
              team_name: str = Query(..., description = "Name of the team (ex: Team A)")):
    team = Team(course_name, team_name)
    if not os.path.exists(team.info_file):
        return {"message": f"Team '{team_name}' not found in course '{course_name}'."}
    
    with open(team.info_file, "r", encoding = "utf-8") as f:
        info = f.read().splitlines()
    
    return {
        "course": course_name,
        "team": team_name,
        "detail": info
    }


router.add_api_route(
    path = "/create", #요청 주소
    endpoint = create_team, #실행할 함수
    methods = ["POST"], #HTTP 메소드
    summary = "create team" #swagger ui에 표시될 이름
)

router.add_api_route(
    path = "/detail", #요청 주소
    endpoint = get_team,#실행할 함수
    methods = ["GET"], #HTTP 메소드
    summary = "get team detail" #swagger ui에 표시될 이름
    )