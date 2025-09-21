import os
import io
import glob
import numpy as np
import pandas as pd
import faiss
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from typing import List

# --- Configurações Iniciais ---

print("Carregando o modelo de geração de texto...")
generator = pipeline("text2text-generation", model="google/flan-t5-small")
print("Modelo carregado com sucesso.")

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dim = 384

index = faiss.IndexFlatIP(dim)
documents = []

def chunk_text(text: str, max_length: int = 500, overlap: int = 50) -> List[str]:
    """
    Divide um texto em chunks menores com overlap para melhor busca semântica.
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_length - overlap):
        chunk = " ".join(words[i:i + max_length])
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks if chunks else [text]

def load_context_files():
    """
    Carrega automaticamente arquivos CSV da pasta 'context/' na inicialização.
    """
    context_dir = "context"
    if not os.path.exists(context_dir):
        print(f"📁 Pasta '{context_dir}' não encontrada. Criando...")
        os.makedirs(context_dir)
        return
    
    csv_files = glob.glob(os.path.join(context_dir, "*.csv"))
    
    if not csv_files:
        print(f"📄 Nenhum arquivo CSV encontrado em '{context_dir}/'")
        return
    
    total_loaded = 0
    
    for csv_file in csv_files:
        try:
            print(f"📚 Carregando contexto de: {os.path.basename(csv_file)}")
            df = pd.read_csv(csv_file)
            
            # Estratégia 1: Coluna 'context' (prioridade)
            if 'context' in df.columns:
                texts = df['context'].dropna().astype(str).tolist()
                source = f"{os.path.basename(csv_file)} (context)"
            
            # Estratégia 2: Primeira coluna de texto
            elif len(df.columns) > 0:
                first_col = df.columns[0]
                texts = df[first_col].dropna().astype(str).tolist()
                source = f"{os.path.basename(csv_file)} ({first_col})"
            
            else:
                print(f"⚠️  Arquivo {csv_file} não possui colunas válidas")
                continue
            
            # Aplicar chunking nos textos
            chunked_texts = []
            
            for text in texts:
                if len(text.strip()) > 0:
                    chunks = chunk_text(text)
                    chunked_texts.extend(chunks)
            
            if chunked_texts:
                # Gerar embeddings e adicionar ao índice
                vecs = embedder.encode(chunked_texts, convert_to_numpy=True, normalize_embeddings=True)
                index.add(vecs)
                documents.extend(chunked_texts)
                
                total_loaded += len(chunked_texts)
                print(f"✅ {len(chunked_texts)} chunks carregados de {os.path.basename(csv_file)}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar {csv_file}: {str(e)}")
    
    if total_loaded > 0:
        print(f"🎉 Total de {total_loaded} chunks de contexto carregados automaticamente!")
    else:
        print("⚠️  Nenhum contexto foi carregado")

# Carregar contextos automaticamente na inicialização
print("\n🔄 Carregando contextos automaticamente...")
load_context_files()

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
    chunks = chunk_text(item.text)
    
    for chunk in chunks:
        vec = embedder.encode([chunk], convert_to_numpy=True, normalize_embeddings=True)
        index.add(vec)
        documents.append(chunk)
    
    return {
        "status": "added", 
        "text": item.text,
        "chunks_created": len(chunks)
    }

@app.post("/ingest-csv/")
async def ingest_csv(file: UploadFile = File(...)):
    """
    Endpoint para ingerir um arquivo CSV.
    Suporta múltiplas estratégias para encontrar o contexto.
    """
    try:
        contents = await file.read()
        buffer = io.BytesIO(contents)
        df = pd.read_csv(buffer)

        # Estratégia 1: Coluna 'context'
        if 'context' in df.columns:
            texts = df['context'].dropna().astype(str).tolist()
            column_used = 'context'
        
        # Estratégia 2: Primeira coluna
        elif len(df.columns) > 0:
            first_col = df.columns[0]
            texts = df[first_col].dropna().astype(str).tolist()
            column_used = first_col
        
        else:
            return {"error": "Arquivo CSV não possui colunas válidas."}

        if not texts:
            return {"error": f"Nenhum texto encontrado na coluna '{column_used}'."}

        # Aplicar chunking e adicionar ao índice
        total_chunks = 0
        for text in texts:
            chunks = chunk_text(text)
            
            for chunk in chunks:
                vec = embedder.encode([chunk], convert_to_numpy=True, normalize_embeddings=True)
                index.add(vec)
                documents.append(chunk)
                total_chunks += 1
        
        return {
            "status": "success", 
            "documents_processed": len(texts),
            "chunks_created": total_chunks,
            "column_used": column_used,
            "filename": file.filename
        }

    except Exception as e:
        return {"error": f"Falha ao processar o arquivo: {str(e)}"}

@app.get("/context/stats")
def get_context_stats():
    """Endpoint para obter estatísticas básicas do contexto carregado."""
    return {
        "total_chunks": len(documents),
        "message": "Base de conhecimento carregada" if documents else "Nenhum contexto carregado"
    }

@app.delete("/context/clear")
def clear_context():
    """Endpoint para limpar toda a base de conhecimento."""
    global index, documents
    
    # Recriar o índice vazio
    index = faiss.IndexFlatIP(dim)
    documents.clear()
    
    return {"status": "cleared", "message": "Base de conhecimento limpa com sucesso"}

@app.post("/ask")
def ask(item: Ask):
    """Endpoint para fazer uma pergunta com busca semântica simplificada."""
    if not documents:
        return {
            "answer": "A base de conhecimento está vazia. Por favor, insira um contexto primeiro.", 
            "context": "Sem contexto disponível."
        }

    # Buscar o contexto mais relevante
    q_vec = embedder.encode([item.question], convert_to_numpy=True, normalize_embeddings=True)
    D, I = index.search(q_vec, 1)
    
    # Selecionar o melhor contexto
    best_context = documents[I[0][0]]

    # Prompt em português
    prompt = f"""Com base no contexto fornecido, responda à pergunta de forma clara e objetiva.

Contexto: {best_context}

Pergunta: {item.question}

Resposta:"""

    try:
        generated = generator(prompt, max_length=150, num_return_sequences=1, do_sample=True, temperature=0.7)
        answer = generated[0]['generated_text']
        
        # Limpar o prompt da resposta se necessário
        if prompt in answer:
            answer = answer.replace(prompt, "").strip()
    
    except Exception as e:
        answer = f"Erro ao gerar resposta: {str(e)}"

    return {
        "answer": answer,
        "context": best_context
    }
