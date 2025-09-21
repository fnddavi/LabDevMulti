#!/usr/bin/env python3
"""
Script de teste para verificar o carregamento automático de contexto.
"""

import requests
import json
import time

# URL da API
API_URL = "http://localhost:8000"

def test_api_health():
    """Testa se a API está funcionando."""
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_context_stats():
    """Testa as estatísticas do contexto carregado."""
    try:
        response = requests.get(f"{API_URL}/context/stats")
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Estatísticas do Contexto:")
            print(f"   Total de chunks: {data['total_chunks']}")
            print(f"   Total de fontes: {data['total_sources']}")
            print("   Fontes:")
            for source, count in data['sources'].items():
                print(f"     - {source}: {count} chunks")
            return True
        else:
            print(f"❌ Erro ao obter estatísticas: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_question(question):
    """Testa uma pergunta específica."""
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"\n❓ Pergunta: {question}")
            print(f"💡 Resposta: {data['answer']}")
            print(f"📝 Contexto usado: {data['context'][:100]}...")
            print(f"🎯 Confiança: {data['confidence']:.3f}")
            if data.get('context_metadata'):
                metadata = data['context_metadata']
                print(f"📋 Fonte: {metadata.get('source', 'N/A')}")
            return True
        else:
            print(f"❌ Erro na pergunta: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    print("🧪 Testando funcionalidades da API...")
    print("=" * 50)
    
    # Aguardar um pouco para a API inicializar
    print("⏱️  Aguardando API inicializar...")
    time.sleep(3)
    
    # Teste 1: Health check
    if not test_api_health():
        print("❌ API não está funcionando. Certifique-se de que está rodando em http://localhost:8000")
        return
    
    # Teste 2: Estatísticas do contexto
    test_context_stats()
    
    # Teste 3: Perguntas sobre o curso DSM
    questions = [
        "O que é o curso DSM?",
        "Quantos semestres tem o curso?",
        "Quais disciplinas são ensinadas no primeiro semestre?",
        "O curso tem estágio obrigatório?",
        "Que tipo de profissional o curso forma?"
    ]
    
    print("\n" + "=" * 50)
    print("🎯 Testando perguntas sobre o curso DSM:")
    
    for question in questions:
        test_question(question)
        time.sleep(1)  # Pequena pausa entre perguntas
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    main()