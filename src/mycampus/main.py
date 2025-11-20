from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mycampus.routers.courses_router import router as courses_router
from mycampus.routers.files_router import router as files_router
from mycampus.routers.assignments_router import router as assignments_router


app = FastAPI()
app.include_router(courses_router)
app.include_router(files_router)
app.include_router(assignments_router)



#프론트엔드: html은 생성형 ai의 도움을 받음
@app.get("/", response_class = HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>MyCampus Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    padding: 60px 16px;
                }
                .container {
                    max-width: 780px;
                    margin: auto;
                    background: #ffffff;
                    padding: 32px 28px;
                    border-radius: 16px;
                    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
                }
                h1 {
                    margin: 0 0 8px 0;
                    color: #222;
                }
                h2 {
                    margin-top: 28px;
                    margin-bottom: 8px;
                    color: #333;
                    font-size: 1.1rem;
                }
                p {
                    color: #555;
                    line-height: 1.5;
                    margin: 4px 0;
                    font-size: 0.95rem;
                }
                a {
                    color: #0066cc;
                    text-decoration: none;
                    font-weight: 500;
                }
                a:hover {
                    text-decoration: underline;
                }
                .router-list {
                    margin-top: 12px;
                }
                .router {
                    margin-top: 12px;
                    padding: 12px 14px;
                    border-radius: 10px;
                    background: #fafafa;
                    border: 1px solid #eee;
                    font-size: 0.95rem;
                }
                .router-title {
                    font-weight: 700;
                    margin-bottom: 5px;
                    font-size: 1rem;
                }
                .path {
                    font-size: 0.9rem;
                    color: #444;
                    line-height: 1.4;
                }
                .footer {
                    margin-top: 28px;
                    font-size: 0.8rem;
                    color: #999;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📚 MyCampus Server</h1>
                <p>FastAPI와 Swagger UI를 사용해 제공되는 학습 관리 API입니다.</p>

                <h2>🧪 API 테스트</h2>
                <p>
                    API 문서는 
                    <a href="/docs" target="_blank">/docs (Swagger UI)</a>
                    에서 확인하고 실행할 수 있습니다.
                </p>

                <h2>🧭 라우터 소개</h2>
                <div class="router-list">
                    <div class="router">
                        <div class="router-title">📂 /courses</div>
                        <div class="path">
                            - 코스 생성<br>
                            - 주차(Week) 생성<br>
                            - 학습 도구(Lecturenote / Assignment / Project) 폴더 생성<br>
                            - 코스 및 폴더 삭제
                        </div>
                    </div>

                    <div class="router">
                        <div class="router-title">📁 /files</div>
                        <div class="path">
                            - 파일 업로드<br>
                            - 파일 다운로드<br>
                            - 파일 삭제
                        </div>
                    </div>

                    <div class="router">
                        <div class="router-title">✅ /assignments</div>
                        <div class="path">
                            - 과제 생성<br>
                            - 과제 목록 조회<br>
                            - 과제 상태 업데이트<br>
                            - 마감일/노트 수정
                        </div>
                    </div>
                </div>

                <div class="footer">MyCampus © 2025</div>
            </div>
        </body>
    </html>
    """