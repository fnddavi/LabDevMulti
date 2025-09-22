#!/bin/bash

# Script de setup - Cria ambiente virtual e instala dependências
# Autor: Fernando Davi
# Data: 21/09/2025

echo "📦 Setup da aplicação LLM..."
echo "============================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se o comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar se Python está instalado
if ! command_exists python3; then
    echo -e "${RED}❌ Python3 não encontrado. Por favor, instale o Python3.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 encontrado${NC}"

# Verificar se curl está instalado (necessário para verificar API)
if ! command_exists curl; then
    echo -e "${YELLOW}⚠️  curl não encontrado. Instalando...${NC}"
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y curl
    elif command_exists yum; then
        sudo yum install -y curl
    elif command_exists dnf; then
        sudo dnf install -y curl
    else
        echo -e "${YELLOW}💡 Por favor, instale curl manualmente para melhor funcionalidade${NC}"
    fi
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Criando ambiente virtual...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro ao criar ambiente virtual.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
else
    echo -e "${GREEN}✅ Ambiente virtual já existe${NC}"
fi

# Ativar ambiente virtual
echo -e "${YELLOW}🔧 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Instalar/Atualizar dependências
echo -e "${YELLOW}📚 Instalando/atualizando dependências...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao instalar dependências.${NC}"
    deactivate
    exit 1
fi

echo -e "${GREEN}✅ Dependências instaladas com sucesso!${NC}"
echo ""
echo -e "${GREEN}🎉 Setup concluído! Agora você pode executar:${NC}"
echo -e "${YELLOW}   ./run_Linux.sh${NC} - Para executar a aplicação"

deactivate