import gradio as gr
import requests

ASK_URL = "http://127.0.0.1:8000/ask"
INGEST_URL = "http://127.0.0.1:8000/ingest"

def perguntar(question):
    payload = {"question": question}
    resp = requests.post(ASK_URL, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        return f"Resposta: {data.get('answer', 'Sem resposta')}\n\nContexto: {data.get('context', '')}"
    else:
        return f"Erro: {resp.text}"

def inserir_contexto(text):
    payload = {"text": text}
    resp = requests.post(INGEST_URL, json=payload)
    if resp.status_code == 200:
        return f"Contexto adicionado: {text}"
    else:
        return f"Erro ao adicionar contexto: {resp.text}"

with gr.Blocks() as demo:
    gr.Markdown("# Interface para API FastAPI (Perguntas e Contexto)")
    with gr.Tab("Perguntar"):
        pergunta = gr.Textbox(label="Pergunta")
        resposta = gr.Textbox(label="Resposta e Contexto")
        btn_perguntar = gr.Button("Enviar Pergunta")
        btn_perguntar.click(perguntar, inputs=pergunta, outputs=resposta)
    with gr.Tab("Inserir Contexto"):
        contexto = gr.Textbox(label="Texto do Contexto")
        saida_contexto = gr.Textbox(label="Status da Inserção")
        btn_contexto = gr.Button("Adicionar Contexto")
        btn_contexto.click(inserir_contexto, inputs=contexto, outputs=saida_contexto)

if __name__ == "__main__":
    demo.launch()
