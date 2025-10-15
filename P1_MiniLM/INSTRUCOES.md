# 📚 Instruções de Uso - Aplicação LLM

## 🔧 Configuração Inicial

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Executar a Aplicação

### Opção 1: Executar apenas a API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

- 📡 API disponível em: <http://localhost:8000>

### Opção 2: Executar apenas a interface web

```bash
streamlit run interface.py --server.port 8501
```

- 🌐 Interface disponível em: <http://localhost:8501>
- ⚠️ Certifique-se de que a API esteja rodando antes

### Opção 3: Executar ambos (recomendado)

**Terminal 1 - API:**

*Windows:*

```bash
venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 8000
```

*Linux/Mac:*

```bash
source venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Interface:**

*Windows:*

```bash
venv\Scripts\activate
streamlit run interface.py --server.port 8501
```

*Linux/Mac:*

```bash
source venv/bin/activate
streamlit run interface.py --server.port 8501
```

## 🌐 Acessar a Aplicação

- **API:** <http://localhost:8000>
- **Interface Web:** <http://localhost:8501>

## 📝 Notas Importantes

- **Ambiente Virtual:** Sempre ative o ambiente virtual antes de executar os comandos
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- **Contextos:** A pasta `context/` contém os arquivos de contexto processados
- **Parar aplicação:** Use `Ctrl+C` no terminal
- **Python:** Certifique-se de ter Python 3.8+ instalado
- **Dependências:** Se houver erro de instalação, tente atualizar o pip primeiro

## 🔍 Verificar se tudo está funcionando

1. Acesse <http://localhost:8000> - deve mostrar a documentação da API
2. Acesse <http://localhost:8501> - deve carregar a interface Streamlit
3. Teste fazendo uma pergunta na interface web
