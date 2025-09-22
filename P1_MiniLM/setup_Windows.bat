@echo off
setlocal

:: Script de setup - Cria ambiente virtual e instala dependências (Windows)
:: Autor: Fernando Davi
:: Data: 21/09/2025

echo.
echo 📦 Setup da aplicacao LLM...
echo ============================
echo.

:: Verificar se Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado. Por favor, instale o Python e adicione ao PATH.
    exit /b 1
)

echo ✅ Python encontrado

:: Verificar se o ambiente virtual existe
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual.
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual ja existe
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call "venv\Scripts\activate.bat"

:: Instalar/Atualizar dependências
echo 📚 Instalando/atualizando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias.
    call "venv\Scripts\deactivate.bat"
    exit /b 1
)

echo ✅ Dependencias instaladas com sucesso!
echo.
echo 🎉 Setup concluido! Agora voce pode executar:
echo    run_Windows.bat - Para executar a aplicacao

call "venv\Scripts\deactivate.bat"
pause