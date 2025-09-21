@echo off
setlocal

:: Script para executar a aplicação LLM com interface web no Windows
:: Autor: Fernando Davi (Adaptado para Windows por Gemini)
:: Data: 21/09/2025

echo.
echo 🚀 Iniciando aplicacao LLM com interface web...
echo ================================================
echo.

:: Função para verificar se o comando existe
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado. Por favor, instale o Python e adicione ao PATH.
    exit /b 1
)

:: Verificar se o ambiente virtual existe
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual.
        exit /b 1
    )
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call "venv\Scripts\activate.bat"

:: Instalar/Atualizar dependências
echo 📚 Instalando dependencias do requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias.
    call "venv\Scripts\deactivate.bat"
    exit /b 1
)

echo ✅ Dependencias instaladas com sucesso!
echo.

:: --- Nome do arquivo da interface ---
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

echo ⏳ Aguardando a API inicializar...
timeout /t 5 >nul

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