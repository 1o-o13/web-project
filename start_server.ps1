# FastAPI 서버 백그라운드 실행 스크립트
$projectPath = "C:\big21\web_project"
Set-Location $projectPath

# .env 파일에서 환경 변수 로드
if (Test-Path .env) {
    $envContent = Get-Content .env
    foreach ($line in $envContent) {
        if ($line -match '^\s*([^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

# 가상환경 활성화
& ".\venv\Scripts\Activate.ps1"

# 서버 실행
python main.py
