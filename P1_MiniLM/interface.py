import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="LLM Chat Interface",
    page_icon="🤖",
    layout="wide"
)

# URL da API FastAPI
API_URL = "http://localhost:8000"

# Título da aplicação
st.title("🤖 Interface Chat com LLM Local")
st.markdown("---")

# Inicializa o session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'contexts_manual' not in st.session_state:
    st.session_state.contexts_manual = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.subheader("📊 Status da API")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            st.success(f"✅ API conectada: {API_URL}")
        else:
            st.error(f"❌ API respondeu com erro: {response.status_code}")
    except requests.exceptions.RequestException:
        st.error("❌ Erro de conexão com a API")
    
    st.markdown("---")
    
    # Seção de gerenciamento de contexto movida para sidebar
    st.header("📚 Gerenciar Contexto")

    # Uploader de arquivo CSV
    st.subheader("Carregar Arquivo (.csv)")
    uploaded_file = st.file_uploader(
        "Arquivo CSV com coluna 'context'", 
        type=['csv']
    )
    if uploaded_file is not None:
        with st.spinner("Processando..."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
                response = requests.post(f"{API_URL}/ingest-csv/", files=files)

                if response.status_code == 200:
                    result = response.json()
                    if "error" in result:
                        st.error(f"❌ Erro: {result['error']}")
                    else:
                        st.success(f"✅ {result.get('documents_added', 0)} contextos adicionados!")
                else:
                    st.error(f"❌ Erro da API: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro de conexão: {e}")
    
    # Formulário para adicionar contexto manual
    st.subheader("Adicionar Contexto Manual")
    with st.form("add_context", clear_on_submit=True):
        context_text = st.text_area("Digite o texto:", height=80)
        submit_context = st.form_submit_button("📝 Adicionar")
        
        if submit_context and context_text:
            try:
                response = requests.post(f"{API_URL}/ingest", json={"text": context_text})
                if response.status_code == 200:
                    st.session_state.contexts_manual.append(context_text)
                    st.success("✅ Contexto adicionado!")
                else:
                    st.error(f"❌ Erro ao adicionar: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro de conexão: {e}")

    # Mostrar contextos manuais adicionados
    if st.session_state.contexts_manual:
        st.subheader("📋 Contextos Adicionados")
        for i, context in enumerate(st.session_state.contexts_manual):
            with st.expander(f"Contexto {i+1}", expanded=False):
                st.write(context[:100] + "..." if len(context) > 100 else context)
    
    st.markdown("---")
    
    # Botões de limpeza
    if st.button("🗑️ Limpar Histórico", type="secondary"):
        st.session_state.contexts_manual = []
        st.session_state.messages = []
        st.rerun()

# Layout principal - apenas o chat
st.header("💬 Chat com o Modelo")

# Exibe o histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Pensando..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={"question": prompt})
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "Sem resposta.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Erro da API: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro de conexão: {e}")
