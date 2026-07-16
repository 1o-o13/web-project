from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv
import models
from database import engine
from routers import auth, contacts, categories

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="연락처 관리 웹 서비스",
    description="FastAPI + PostgreSQL + 세션 로그인",
    version="2.0",
)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(categories.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
