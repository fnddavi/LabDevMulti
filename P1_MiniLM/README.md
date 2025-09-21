# 🤖 LLM Local com Interface Web - Versão Aprimorada

Este projeto implementa uma aplicação de chat inteligente com um modelo de linguagem local usando FastAPI, Streamlit e modelos Hugging Face, com **carregamento automático de contexto** e **busca semântica avançada**.

## ✨ Novas Funcionalidades

### � **Auto-carregamento de Contexto**
- Carrega automaticamente arquivos CSV da pasta `context/` na inicialização
- Suporta múltiplas estratégias para encontrar contexto em CSVs
- Chunking inteligente para textos longos (melhor busca semântica)

### 🔍 **Busca Semântica Avançada**
- Busca por múltiplos contextos relevantes
- Score de confiança para cada resposta
- Metadados detalhados sobre a fonte do contexto
- Contextos alternativos para transparência

### 🎛️ **Gerenciamento de Contexto**
- Endpoint para estatísticas da base de conhecimento
- Limpeza da base de conhecimento via API
- Interface web mostra fontes e chunks carregados

## 📋 Características Principais

- **API FastAPI**: Backend robusto com endpoints avançados
- **Interface Streamlit**: Frontend limpo e intuitivo focado na conversação
- **Modelo Local**: Usa Flan-T5-Small para geração de texto em português
- **Busca FAISS**: Implementa busca por similaridade otimizada
- **Chunking Inteligente**: Divide textos longos automaticamente
- **Embeddings**: Utiliza sentence-transformers para vetorização

## 🚀 Instalação e Execução

### Método Automático (Recomendado)

```bash
# Executa API e interface web
./run.sh

# Ou especifique o que executar:
./run.sh api    # Apenas API
./run.sh web    # Apenas interface web  
./run.sh both   # Ambos (padrão)
```

### Método Manual

1. **Criar ambiente virtual:**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

3. **Executar API:**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

4. **Executar interface web (em outro terminal):**

```bash
streamlit run interface.py --server.port 8501
```

## 🌐 Acesso

- **API FastAPI**: <http://localhost:8000>
- **Documentação da API**: <http://localhost:8000/docs>
- **Interface Web**: <http://localhost:8501>

## 💻 Como Usar

### 1. **Auto-carregamento (Novo!)**

- Coloque arquivos CSV na pasta `context/`
- A API carregará automaticamente na inicialização
- Suporta colunas `context` ou primeira coluna disponível

### 2. **Upload de CSV via Interface**

- Use o upload de arquivo na interface web
- Suporta múltiplos formatos de CSV
- Feedback detalhado sobre o processamento

### 3. **Adicionar Contexto Manual**

- Digite textos diretamente na interface
- Chunking automático para textos longos

### 4. **Fazer Perguntas**

- Chat interativo com histórico
- Interface limpa e focada na resposta
- Respostas baseadas no contexto mais relevante

### 5. **Via API (Avançado)**

```bash
# Verificar estatísticas
curl http://localhost:8000/context/stats

# Adicionar contexto
curl -X POST "http://localhost:8000/ingest" \
     -H "Content-Type: application/json" \
     -d '{"text": "Seu texto aqui"}'

# Fazer pergunta
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Sua pergunta"}'

# Limpar base de conhecimento
curl -X DELETE "http://localhost:8000/context/clear"
```

## 📁 Estrutura do Projeto

```
├── app.py                    # API FastAPI com funcionalidades avançadas
├── interface.py             # Interface Streamlit aprimorada
├── requirements.txt         # Dependências Python
├── run.sh                  # Script de execução automática
├── test_api.py             # Script de teste das funcionalidades
├── context/                # Pasta para arquivos CSV (auto-carregamento)
│   ├── curso_DSM_FATEC_com_matriz_with_context.csv
│   └── curso_DSM_FATEC_context_only.csv
└── README.md               # Este arquivo
```

## 🧪 Testando a Aplicação

Execute o script de teste para verificar todas as funcionalidades:

```bash
# Inicie a API primeiro
./run.sh api

# Em outro terminal, execute os testes
python test_api.py
```

## 🔧 Dependências Principais

- **FastAPI**: Framework web para API
- **Streamlit**: Framework para interface web
- **Transformers**: Modelos Hugging Face (Flan-T5-Small)
- **Sentence-Transformers**: Embeddings de texto (all-MiniLM-L6-v2)
- **FAISS**: Busca por similaridade vetorial
- **Pandas**: Processamento de dados CSV
- **NumPy**: Operações numéricas

## 📊 Endpoints da API

### Principais:
- `GET /` - Health check
- `POST /ingest` - Adicionar contexto individual
- `POST /ingest-csv/` - Upload de arquivo CSV
- `POST /ask` - Fazer pergunta
- `GET /context/stats` - Estatísticas da base
- `DELETE /context/clear` - Limpar base

### Novos Recursos de Resposta:
- **Confiança**: Score de similaridade semântica
- **Metadados**: Informações sobre fonte e chunking
- **Contextos Alternativos**: Outros contextos relevantes
- **Chunking**: Divisão automática de textos longos

## ⚠️ Considerações

- **Primeira execução**: Modelos serão baixados (≈200MB total)
- **Chunking**: Textos longos são divididos automaticamente (500 palavras/chunk)
- **Performance**: Modelo Flan-T5-Small é rápido e eficiente
- **Contexto**: CSVs são carregados automaticamente da pasta `context/`
- **Memória**: Índice FAISS permanece em memória (reiniciar limpa tudo)

## 🐛 Solução de Problemas

1. **Pasta context/ não existe**: Será criada automaticamente
2. **Modelo não carrega**: Verifique conexão de internet na primeira vez
3. **CSV não carrega**: Verifique se tem coluna 'context' ou dados válidos
4. **Interface não conecta**: Certifique-se de que API está em localhost:8000
5. **Respostas vazias**: Verifique se contexto foi carregado via `/context/stats`

## 📈 Melhorias Implementadas

✅ **Auto-carregamento** de contexto na inicialização  
✅ **Chunking inteligente** para textos longos  
✅ **Busca semântica** com múltiplos resultados  
✅ **Metadados detalhados** sobre contextos  
✅ **Score de confiança** para respostas  
✅ **Gerenciamento** via endpoints RESTful  
✅ **Interface aprimorada** com métricas visuais  
✅ **Suporte robusto** a múltiplos formatos CSV  

## 📝 Licença

Este projeto é para fins educacionais e de demonstração.