import os
import requests
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv  # <-- Adicionado para carregar variáveis de ambiente

load_dotenv()

# --- Configurações Iniciais ---

# Carrega a chave da API do Hugging Face a partir das variáveis de ambiente
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Define o modelo de LLM que será usado para geração de texto
HF_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Carrega o modelo de embeddings para vetorizar o texto
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dim = 384  # Dimensão dos vetores gerados pelo modelo de embedding

# Cria um índice FAISS para armazenar e buscar os vetores de forma eficiente
index = faiss.IndexFlatIP(dim)

# Lista para armazenar os documentos de texto originais
documents = []

# --- Inicialização da API FastAPI ---
app = FastAPI()


# --- Modelos de Dados Pydantic ---
class Ingest(BaseModel):
    text: str


class Ask(BaseModel):
    question: str


# --- Endpoints da API ---


@app.post("/ingest")
def ingest(item: Ingest):
    """
    Endpoint para adicionar um novo texto à base de conhecimento.
    """
    # Gera o embedding para o texto recebido
    vec = embedder.encode([item.text], convert_to_numpy=True, normalize_embeddings=True)

    # Adiciona o vetor ao índice FAISS e o texto à lista de documentos
    index.add(vec)
    documents.append(item.text)

    return {"status": "added", "text": item.text}


@app.post("/ask")
def ask(item: Ask):
    """
    Endpoint para fazer uma pergunta e obter uma resposta gerada pelo LLM.
    """
    # Gera o embedding para a pergunta
    q_vec = embedder.encode(
        [item.question], convert_to_numpy=True, normalize_embeddings=True
    )

    # Busca no índice FAISS pelo vetor mais similar (top 1)
    D, I = index.search(q_vec, 1)

    # Recupera o texto original correspondente ao vetor encontrado
    context = documents[I[0][0]] if len(documents) > 0 else "Sem contexto disponível."

    # Monta o prompt combinando o contexto recuperado com a pergunta do usuário [cite: 12, 19]
    prompt = f"Contexto: {context}\n\nPergunta: {item.question}\nResposta:"

    # --- Chamada à Hugging Face Inference API ---

    # Define os cabeçalhos para autenticação
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    # Define o payload da requisição com o prompt e parâmetros de geração
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200},  # Limita o tamanho da resposta
    }

    # Realiza a chamada POST para o modelo no Hugging Face
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload,
    )
    data = resp.json()

    # Extrai a resposta gerada do JSON retornado pela API
    try:
        data = resp.json()
        answer = data[0]["generated_text"] if isinstance(data, list) else str(data)
    except requests.exceptions.JSONDecodeError:
        answer = "Erro ao processar a resposta da API. O modelo pode estar carregando. Tente novamente em um minuto."
    except (KeyError, IndexError):
        answer = f"A API retornou uma resposta inesperada: {resp.text}"

    return {"answer": answer, "context": context}
