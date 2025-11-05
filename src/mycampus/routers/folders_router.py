from fastapi import APIRouter, HTTPException 
#APIROUTER: ROUTER객체를 만들 때 쓰는 클래스, HTTPException: API 실행 중 문제 생겼을 때 오류 코드 반환할 때 쓰는 클래스
from pydantic import BaseModel, field_validator
#BaseModel: 데이터 구조를 정의하고 검증할 때 쓰는 클래스, field_validator: 입력값을 검증, 정제할 때 쓰는 "데코레이터 : 기존 함수에 새로운 기능 추가하는 것"
from typing import Optional
#Optional: 값이 있을 수도 있고 없을 수도 있는 경우를 나타낼 때 쓰는 타입 힌트, ex) week:Optional[int] = None -> week가 int형 값이거나 None일 수 있음
from pathlib import path
#pathlib: python의 파일/폴더 경로를 다루는 표준 라이브러리, path: 파일 및 디렉토리 경로를 나타내는 클래스 (windows \, linux / )

