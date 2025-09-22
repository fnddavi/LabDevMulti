import pandas as pd
import nltk
import re

# Baixar os modelos necessários para a tokenização
for resource in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        print(f"Baixando o pacote '{resource}' do NLTK...")
        nltk.download(resource)
        print(f"Download de '{resource}' concluído.")



def limpar_e_dividir_texto(texto):
    """
    Função para limpar e dividir um bloco de texto em chunks (sentenças).
    """
    # Substituir múltiplos espaços/quebras de linha por um único espaço
    texto = re.sub(r"\s+", " ", texto).strip()

    # Usar NLTK para dividir o texto em sentenças
    sentencas = nltk.sent_tokenize(texto, language="portuguese")

    chunks_limpos = []
    for sent in sentencas:
        # Ignorar sentenças muito curtas ou irrelevantes
        if len(sent) > 15:  # Filtra sentenças com menos de 15 caracteres
            chunks_limpos.append(sent.strip())

    return chunks_limpos


# --- CONFIGURAÇÃO ---
# Escolha o arquivo de entrada e o nome do arquivo de saída
ARQUIVO_ENTRADA = "curso_DSM_FATEC_context_only.csv"
# ou 'curso_DSM_FATEC_com_matriz_with_context.csv'
ARQUIVO_SAIDA = "contextos_processados.csv"
COLUNA_ALVO = "context"  # Nome da coluna que contém o texto

# Carregar o arquivo CSV original
print(f"Carregando dados de '{ARQUIVO_ENTRADA}'...")
try:
    df_original = pd.read_csv(ARQUIVO_ENTRADA)
except FileNotFoundError:
    print(f"Erro: Arquivo '{ARQUIVO_ENTRADA}' não encontrado.")
    exit()

if COLUNA_ALVO not in df_original.columns:
    print(f"Erro: A coluna '{COLUNA_ALVO}' não foi encontrada no arquivo CSV.")
    exit()

# Lista para armazenar todos os chunks de todos os documentos
todos_os_chunks = []

print("Processando textos e criando chunks...")
# Iterar sobre cada linha do DataFrame original
for texto_bloco in df_original[COLUNA_ALVO].dropna():
    chunks = limpar_e_dividir_texto(texto_bloco)
    todos_os_chunks.extend(chunks)

# Criar um novo DataFrame com os chunks processados
df_processado = pd.DataFrame(todos_os_chunks, columns=[COLUNA_ALVO])

# Salvar o novo DataFrame em um novo arquivo CSV
df_processado.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8")

print("-" * 50)
print(f"✅ Pré-processamento concluído com sucesso!")
print(f"Total de {len(df_original)} blocos de texto originais.")
print(f"Gerados {len(df_processado)} chunks de contexto no novo arquivo.")
print(f"Arquivo salvo como: '{ARQUIVO_SAIDA}'")
print("-" * 50)

# Exibir as 5 primeiras linhas do resultado
print("\nAmostra do resultado:")
print(df_processado.head())
