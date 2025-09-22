@echo off
setlocal

:: Script para executar a aplicação LLM com interface web no Windows
:: Autor: Fernando Davi
:: Data: 21/09/2025

echo.
echo 🚀 Iniciando aplicacao LLM com interface web...
echo ================================================
echo.

:: Verificar se o ambiente virtual existe
if not exist "venv" (
    echo ❌ Ambiente virtual nao encontrado.
    echo 💡 Execute primeiro: setup_Windows.bat
    exit /b 1
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call "venv\Scripts\activate.bat"

:: Verificar se as dependências estão instaladas
python -c "import fastapi, streamlit, sentence_transformers, transformers, faiss" >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencias nao instaladas.
    echo 💡 Execute primeiro: setup_Windows.bat
    call "venv\Scripts\deactivate.bat"
    exit /b 1
)

echo ✅ Ambiente configurado!
echo.

:: Nome do arquivo da interface
set "INTERFACE_FILE=interface.py"

:: Verificar qual opção o usuário quer
if /i "%1"=="api" (
    echo 🚀 Iniciando apenas a API FastAPI...
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
) else if /i "%1"=="web" (
    echo 🌐 Iniciando apenas a interface web...
    echo ⚠️  Certifique-se de que a API esta rodando em http://localhost:8000
    streamlit run "%INTERFACE_FILE%" --server.port 8501
) else if /i "%1"=="both" (
    goto both_case
) else if "%1"=="" (
    goto both_case
) else (
    echo Opcao invalida: %1
    echo.
    echo Uso: %0 [api^|web^|both]
    echo.
    echo Opcoes:
    echo   api     - Inicia apenas a API FastAPI
    echo   web     - Inicia apenas a interface Streamlit
    echo   both    - Inicia API e interface (padrao)
    echo.
    echo Exemplos:
    echo   %0         # Inicia ambos
    echo   %0 api      # Inicia apenas API
    echo   %0 web      # Inicia apenas interface
    goto:eof
)

:both_case
echo 🚀 Iniciando API e Interface Web em paralelo...
echo.

echo 📡 Iniciando API FastAPI em background...
start "FastAPI_API" /B uvicorn app:app --host 0.0.0.0 --port 8000

echo ⏳ Aguardando API carregar contextos e ficar pronta...
set /a max_attempts=30
set /a attempt=0

:wait_loop
set /a attempt+=1
echo    Tentativa %attempt%/%max_attempts%...

:: Verificar se a API responde
curl -s http://localhost:8000/ >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ API esta pronta!
    goto api_ready
)

if %attempt% geq %max_attempts% (
    echo ❌ Timeout: API nao ficou pronta em 60 segundos
    taskkill /F /IM uvicorn.exe >nul 2>nul
    exit /b 1
)

timeout /t 2 >nul
goto wait_loop

:api_ready
echo 🌐 Iniciando interface Streamlit...
start "Streamlit_Web" /B streamlit run "%INTERFACE_FILE%" --server.port 8501

echo.
echo ✅ Aplicacao iniciada com sucesso!
echo    📡 API disponivel em: http://localhost:8000
echo    🌐 Interface web em:  http://localhost:8501
echo.
echo Para parar a aplicacao, feche este terminal.
echo.

:: Mantem o terminal aberto para que os processos em background não fechem
pause

endlocal