## 5. Executando FastAPI e Gradio juntos

Para rodar a API e a interface web ao mesmo tempo, siga estes passos:

1. Abra dois terminais e ative o ambiente virtual em ambos:
	```powershell
	.\venv\Scripts\Activate.ps1
	```

2. No primeiro terminal, inicie o servidor FastAPI:
	```powershell
	uvicorn app:app --reload
	```

3. No segundo terminal, execute a interface Gradio:
	```powershell
	python gradio_app.py
	```

Assim, você poderá acessar a interface web e interagir com a API simultaneamente.
# Guia Rápido de Instalação e Execução

Este projeto utiliza Python e um ambiente virtual para isolar as dependências. Siga os passos abaixo conforme seu sistema operacional.

## 1. Crie o ambiente virtual

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/Ubuntu

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Execute o projeto

```bash
python app.py
```

---


## 4. Interface Web (Gradio)

Você pode utilizar uma interface web simples para inserir contexto e fazer perguntas à API:

1. Instale o Gradio (se ainda não instalou):
	```bash
	pip install gradio
	```

2. Execute o arquivo da interface:
	```bash
	python gradio_app.py
	```

3. Acesse o endereço exibido no terminal (geralmente http://127.0.0.1:7860) para usar a interface.

Na interface, utilize a aba "Inserir Contexto" para adicionar textos à base de conhecimento e a aba "Perguntar" para fazer perguntas e receber respostas.

---

> Dica: Para desativar o ambiente virtual, use `deactivate` no terminal.

Se encontrar problemas, verifique se o Python está instalado e disponível no PATH.
