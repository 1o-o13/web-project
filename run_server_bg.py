"""
FastAPI 서버를 백그라운드에서 실행하는 스크립트
"""
import subprocess
import sys
import os
import time

def start_server():
    """FastAPI 서버 시작"""
    os.chdir(r"C:\big21\web_project")

    # 가상환경 Python 경로
    python_exe = r"C:\big21\web_project\venv\Scripts\python.exe"

    # main.py 실행 (백그라운드 프로세스로)
    process = subprocess.Popen(
        [python_exe, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print(f"✓ FastAPI 서버 시작됨 (PID: {process.pid})")
    print(f"  http://127.0.0.1:8000 으로 접속하세요")
    print(f"  Claude Code를 닫아도 브라우저에서 계속 접속 가능합니다")

    return process

if __name__ == "__main__":
    start_server()
