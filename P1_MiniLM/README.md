# 🤖 Chat LLM com Contexto

Sistema de chat inteligente que permite fazer perguntas sobre documentos usando modelos de IA locais.

## 🧠 Como Funciona

O sistema utiliza:
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` para entender o contexto
- **Geração de Texto**: `google/flan-t5-small` para responder perguntas
- **Busca Semântica**: FAISS para encontrar informações relevantes
- **Interface**: Streamlit para chat web + FastAPI como backend

## 🚀 Como Usar

### Linux

1. **Primeira vez** (instalação):
```bash
./setup_Linux.sh
```

2. **Execução** (sempre que quiser usar):
```bash
./run_Linux.sh
```

### Windows

1. **Primeira vez** (instalação):
```cmd
setup_Windows.bat
```

2. **Execução** (sempre que quiser usar):
```cmd
run_Windows.bat
```

## 📁 Gerenciamento de Contextos

### Localização dos Contextos

Os arquivos de contexto ficam na pasta:
```
context/
├── arquivo1.csv
├── arquivo2.csv
└── ...
```

### Como Adicionar Novos Contextos

#### Método 1: Automático
1. Coloque arquivos `.csv` na pasta `context/`
2. Reinicie o sistema
3. O contexto será carregado automaticamente

#### Método 2: Via Interface
1. Abra a interface web
2. Use o menu lateral "📁 Gerenciar Contexto"
3. Faça upload de arquivos CSV
4. Ou adicione texto manualmente

### Formato dos Arquivos CSV

Os arquivos CSV devem conter uma coluna com o texto/contexto:
```csv
content
"Primeiro parágrafo de contexto..."
"Segundo parágrafo de contexto..."
```

## 💡 Exemplo de Uso

1. Execute o sistema
2. Adicione contextos (CSV ou texto)
3. Faça perguntas como:
   - "O que diz sobre vendas?"
   - "Resuma as principais informações"
   - "Quais são os pontos importantes?"

O sistema encontrará as informações relevantes e gerará respostas baseadas no contexto fornecido.