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

# --- Configurações Iniciais ---

print("Carregando o modelo de geração de texto...")
generator = pipeline("text2text-generation", model="google/flan-t5-small")
print("Modelo carregado com sucesso.")

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dim = 384

index = faiss.IndexFlatIP(dim)
documents = []


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
            if "context" in df.columns:
                texts = df["context"].dropna().astype(str).tolist()

            # Estratégia 2: Primeira coluna de texto
            elif len(df.columns) > 0:
                first_col = df.columns[0]
                texts = df[first_col].dropna().astype(str).tolist()

            else:
                print(f"⚠️  Arquivo {csv_file} não possui colunas válidas")
                continue

            # Filtrar textos vazios
            valid_texts = [text for text in texts if len(text.strip()) > 0]

            if valid_texts:
                # Gerar embeddings e adicionar ao índice
                vecs = embedder.encode(
                    valid_texts, convert_to_numpy=True, normalize_embeddings=True
                )
                index.add(vecs)
                documents.extend(valid_texts)

                total_loaded += len(valid_texts)
                print(
                    f"✅ {len(valid_texts)} contextos carregados de {os.path.basename(csv_file)}"
                )

        except Exception as e:
            print(f"❌ Erro ao carregar {csv_file}: {str(e)}")

    if total_loaded > 0:
        print(f"🎉 Total de {total_loaded} contextos carregados automaticamente!")
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
    vec = embedder.encode([item.text], convert_to_numpy=True, normalize_embeddings=True)
    index.add(vec)
    documents.append(item.text)

    return {"status": "added", "text": item.text}


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
        if "context" in df.columns:
            texts = df["context"].dropna().astype(str).tolist()
            column_used = "context"

        # Estratégia 2: Primeira coluna
        elif len(df.columns) > 0:
            first_col = df.columns[0]
            texts = df[first_col].dropna().astype(str).tolist()
            column_used = first_col

        else:
            return {"error": "Arquivo CSV não possui colunas válidas."}

        if not texts:
            return {"error": f"Nenhum texto encontrado na coluna '{column_used}'."}

        # Adicionar textos diretamente ao índice
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
        return {
            "answer": "A base de conhecimento está vazia. Por favor, insira um contexto primeiro.",
            "context": "Sem contexto disponível.",
        }

    # Busca semântica
    k_neighbors = min(3, len(documents))
    q_vec = embedder.encode(
        [item.question], convert_to_numpy=True, normalize_embeddings=True
    )
    D, I = index.search(q_vec, k_neighbors)

    best_score = D[0][0]
    best_context_index = I[0][0]

    # --- NOVA VERIFICAÇÃO ---
    # Defina um limiar de similaridade. Para embeddings normalizados e IndexFlatIP,
    # o score varia de -1 a 1. Um valor como 0.5 é um bom ponto de partida.
    SIMILARITY_THRESHOLD = 0.5

    if best_score < SIMILARITY_THRESHOLD:
        return {
            "answer": f"Desculpe, não encontrei informações suficientemente relevantes sobre '{item.question}' na minha base de dados.",
            "context": "Nenhum contexto relevante encontrado.",
        }
    # --- FIM DA VERIFICAÇÃO ---

    best_context = documents[best_context_index]

    prompt = f"""Você é um assistente especializado no curso DSM.
Responda sempre em português, usando apenas o contexto fornecido.

Contexto: {best_context}

Pergunta: {item.question}

Resposta em Português:"""

    try:
        generated = generator(
            prompt,
            max_length=150,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
        )
        answer = generated[0]["generated_text"]

        if prompt in answer:
            answer = answer.replace(prompt, "").strip()

    except Exception as e:
        answer = f"Erro ao gerar resposta: {str(e)}"

    return {"answer": answer, "context": best_context}
