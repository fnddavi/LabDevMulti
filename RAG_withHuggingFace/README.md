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

> Dica: Para desativar o ambiente virtual, use `deactivate` no terminal.

Se encontrar problemas, verifique se o Python está instalado e disponível no PATH.
