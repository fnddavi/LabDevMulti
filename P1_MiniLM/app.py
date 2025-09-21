import os
import io
import numpy as np
import pandas as pd
import faiss
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# --- Configurações Iniciais ---

print("Carregando o modelo de geração de texto...")
generator = pipeline("text2text-generation", model="google/flan-t5-small")
print("Modelo carregado com sucesso.")

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dim = 384

index = faiss.IndexFlatIP(dim)
documents = []

# --- API FastAPI ---
app = FastAPI()

@app.get("/")
def health_check():
    """Endpoint para verificar se a API está no ar."""
    return {"status": "ok", "message": "API está funcionando corretamente!"}

# --- Modelos de Dados ---
class Ingest(BaseModel):
    text: str

class Ask(BaseModel):
    question: str

# --- Endpoints ---

@app.post("/ingest")
def ingest(item: Ingest):
    """Endpoint para adicionar um novo texto à base de conhecimento."""
    vec = embedder.encode([item.text], convert_to_numpy=True, normalize_embeddings=True)
    index.add(vec)
    documents.append(item.text)
    return {"status": "added", "text": item.text}

@app.post("/ingest-csv/")
async def ingest_csv(file: UploadFile = File(...)):
    """
    Endpoint para ingerir um arquivo CSV.
    Assume que o texto a ser indexado está em uma coluna chamada 'context'.
    """
    try:
        contents = await file.read()
        buffer = io.BytesIO(contents)
        df = pd.read_csv(buffer)

        if 'context' not in df.columns:
            return {"error": "Arquivo CSV deve conter uma coluna 'context'."}

        texts = df['context'].dropna().astype(str).tolist()
        
        if not texts:
            return {"error": "Nenhum texto encontrado na coluna 'context'."}

        vecs = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        index.add(vecs)
        documents.extend(texts)
        
        return {"status": "success", "documents_added": len(texts)}

    except Exception as e:
        return {"error": f"Falha ao processar o arquivo: {str(e)}"}

@app.post("/ask")
def ask(item: Ask):
    """Endpoint para fazer uma pergunta e obter uma resposta gerada pelo LLM local."""
    if not documents:
        return {"answer": "A base de conhecimento está vazia. Por favor, insira um contexto primeiro.", "context": "Sem contexto disponível."}

    # --- MELHORIA 1: Buscar mais documentos de contexto (k=3) ---
    K_NEIGHBORS = 3
    if index.ntotal < K_NEIGHBORS:
        # Se houver menos documentos do que o K desejado, busca todos
        K_NEIGHBORS = index.ntotal

    q_vec = embedder.encode(
        [item.question], convert_to_numpy=True, normalize_embeddings=True
    )
    D, I = index.search(q_vec, K_NEIGHBORS)
    
    # Juntar os contextos encontrados
    retrieved_contexts = [documents[i] for i in I[0]]
    context = "\n---\n".join(retrieved_contexts)

    # --- MELHORIA 2: Prompt mais claro e direto ---
    # Instruímos o modelo de forma explícita e terminamos com "Resposta:"
    # para guiar a geração.
    prompt = f"""Com base no contexto fornecido, responda a pergunta de forma clara e concisa.

Contexto:
{context}

Pergunta:
{item.question}

Resposta:
"""

    # --- MELHORIA 3: Adicionar 'temperature' para respostas mais focadas ---
    generated = generator(prompt, max_length=150, num_return_sequences=1, temperature=0.1)
    answer = generated[0]['generated_text']

    return {"answer": answer, "context": context}
