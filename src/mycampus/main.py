from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mycampus.routers.courses_router import router as courses_router
from mycampus.routers.files_router import router as files_router
from mycampus.routers.assignments_router import router as assignments_router
from mycampus.routers.team_router import router as team_router


app = FastAPI()
app.include_router(courses_router)
app.include_router(files_router)
app.include_router(assignments_router)
app.include_router(team_router)



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
                    max-width: 820px;
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
                    margin-top: 26px;
                    margin-bottom: 8px;
                    color: #333;
                    font-size: 1.05rem;
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

                .router {
                    margin-top: 14px;
                    padding: 14px 16px;
                    border-radius: 10px;
                    background: #fafafa;
                    border: 1px solid #eee;
                }
                .router-title {
                    font-weight: 700;
                    font-size: 1rem;
                    margin-bottom: 6px;
                    color: #222;
                }
                .routes-mini {
                    font-size: 0.9rem;
                    color: #444;
                    line-height: 1.45;
                }
                code {
                    font-family: Consolas, monospace;
                    background: #eee;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                }
                .footer {
                    margin-top: 32px;
                    font-size: 0.8rem;
                    color: #999;
                }
            </style>
        </head>

        <body>
            <div class="container">
                <h1>📚 MyCampus Server</h1>
                <p>FastAPI와 Swagger UI 기반의 학습 관리 API 서버입니다.</p>

                <h2>🧪 API 문서 (Swagger UI)</h2>
                <p><a href="/docs" target="_blank">/docs</a> 에서 모든 기능을 테스트할 수 있습니다.</p>

                <h2>🧭 라우터 소개</h2>

                <div class="router">
                    <div class="router-title">📂 /courses</div>
                    <div class="routes-mini">
                        - <code>POST /create</code> : 코스·주차·학습도구 폴더 생성<br>
                        - <code>DELETE /delete</code> : 폴더 삭제
                    </div>
                </div>

                <div class="router">
                    <div class="router-title">📁 /files</div>
                    <div class="routes-mini">
                        - <code>POST /upload</code> : 파일 업로드<br>
                        - <code>GET /download</code> : 파일 다운로드<br>
                        - <code>DELETE /delete</code> : 파일 삭제<br>
                        - <code>GET /list</code> : 파일 목록 조회
                    </div>
                </div>

                <div class="router">
                    <div class="router-title">✅ /assignments</div>
                    <div class="routes-mini">
                        - <code>POST /create</code> : 과제 생성<br>
                        - <code>GET /list</code> : 과제 목록 조회<br>
                        - <code>DELETE /delete</code> : 과제 삭제<br>
                        - <code>PUT /status</code> : 상태·마감일·노트 수정
                    </div>
                </div>

                <div class="router">
                    <div class="router-title">👥 /teams</div>
                    <div class="routes-mini">
                        - <code>POST /create</code> : 팀 생성<br>
                        - <code>GET /detail</code> : 팀 정보 조회
                    </div>
                </div>

                <div class="footer">MyCampus © 2025</div>
            </div>
        </body>
    </html>
    """