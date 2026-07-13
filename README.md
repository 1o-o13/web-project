# 연락처 관리 웹 서비스 (v2 - FastAPI)

FastAPI + PostgreSQL 기반 멀티유저 연락처 관리 웹 애플리케이션

## 기술 스택
- **백엔드**: FastAPI 0.139.0, SQLAlchemy 2.0.51, Pydantic 2.13.4
- **DB**: PostgreSQL 16 (Docker)
- **인증**: 세션 쿠키 (Argon2 해싱)
- **프론트**: HTML5 + Vanilla JavaScript (SPA)

## 빠른 시작

### 1. PostgreSQL 실행 (Docker)
```bash
docker run --name pg-lab -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=contactdb -p 5432:5432 -d postgres:16
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. 접속
- **웹 화면**: http://127.0.0.1:8000
- **API 문서**: http://127.0.0.1:8000/docs (Swagger UI)

## 구현 상태
- [ ] 1단계: 프로젝트 구조 & 설정
- [ ] 2단계: Models (4개 테이블)
- [ ] 3단계: Schemas (검증)
- [ ] 4단계: Database (연결)
- [ ] 5단계: Security (해싱)
- [ ] 6단계: CRUD (함수)
- [ ] 7단계: Routers (API)
- [ ] 8단계: Main (앱)
- [ ] 9단계: Static (화면)
- [ ] 10단계: 테스트 & 실행
