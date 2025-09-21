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

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    api_url = st.text_input("URL da API", value=API_URL)
    st.markdown("---")
    
    # Status da API
    st.subheader("📊 Status da API")
    try:
        response = requests.get(f"{api_url}/", timeout=5)
        if response.status_code == 200:
            st.success("✅ API conectada")
            
            # Mostrar estatísticas do contexto
            try:
                stats_response = requests.get(f"{api_url}/context/stats", timeout=5)
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    st.info(f"📚 {stats['total_chunks']} chunks carregados")
                else:
                    st.warning("⚠️ Erro ao obter estatísticas")
            except:
                st.warning("⚠️ Erro ao conectar com /context/stats")
                
        else:
            st.error("❌ API não responde")
    except:
        st.error("❌ Erro de conexão")
    
    st.markdown("---")
    
    # Botão para limpar contexto
    if st.button("🗑️ Limpar Base de Conhecimento", type="secondary"):
        try:
            response = requests.delete(f"{api_url}/context/clear", timeout=10)
            if response.status_code == 200:
                st.success("✅ Base de conhecimento limpa!")
                st.rerun()
            else:
                st.error("❌ Erro ao limpar base")
        except:
            st.error("❌ Erro de conexão")

# Inicializa o session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'contexts_manual' not in st.session_state:
    st.session_state.contexts_manual = []

# Layout principal
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📚 Gerenciar Contexto")

    # Uploader de arquivo CSV
    st.subheader("Carregar Arquivo de Contexto (.csv)")
    uploaded_file = st.file_uploader(
        "Selecione um arquivo CSV com uma coluna chamada 'context'", 
        type=['csv']
    )
    if uploaded_file is not None:
        with st.spinner("Processando arquivo..."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
                response = requests.post(f"{api_url}/ingest-csv/", files=files)

                if response.status_code == 200:
                    result = response.json()
                    if "error" in result:
                        st.error(f"❌ Erro no arquivo: {result['error']}")
                    else:
                        st.success(f"✅ Arquivo processado! {result.get('documents_added', 0)} contextos adicionados.")
                else:
                    st.error(f"❌ Erro da API: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro de conexão: {e}")
    
    # Formulário para adicionar contexto manual
    with st.form("add_context", clear_on_submit=True):
        st.subheader("Adicionar Contexto Manualmente")
        context_text = st.text_area("Digite um trecho de texto:", height=100)
        submit_context = st.form_submit_button("📝 Adicionar Texto")
        
        if submit_context and context_text:
            try:
                response = requests.post(f"{api_url}/ingest", json={"text": context_text})
                if response.status_code == 200:
                    st.session_state.contexts_manual.append(context_text)
                    st.success("✅ Contexto adicionado!")
                else:
                    st.error(f"❌ Erro ao adicionar: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erro de conexão: {e}")

    if st.session_state.contexts_manual:
        st.subheader("📋 Contextos Manuais Adicionados")
        for i, context in enumerate(st.session_state.contexts_manual):
            with st.expander(f"Contexto {i+1}"):
                st.write(context)
    
    if st.button("🗑️ Limpar Histórico Local"):
        st.session_state.contexts_manual = []
        st.session_state.messages = []
        st.rerun()

with col2:
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
                    response = requests.post(f"{api_url}/ask", json={"question": prompt})
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("answer", "Sem resposta.")
                        context_used = result.get("context", "Sem contexto")
                        confidence = result.get("confidence", 0.0)
                        context_metadata = result.get("context_metadata", {})
                        alternative_contexts = result.get("alternative_contexts", [])
                        
                        # Exibir apenas a resposta
                        st.markdown(answer)
                        
                        # Adicionar ao histórico (versão simplificada)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer
                        })
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Erro da API: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão: {e}")
