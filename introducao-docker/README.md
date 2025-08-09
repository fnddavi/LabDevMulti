## Introdução ao Docker

Este diretório contém dois projetos Node.js desenvolvidos como exemplos práticos para a aula de **Introdução ao Docker**.

Cada projeto está em uma pasta separada:

- [`exemplo-um`](./exemplo-um): exemplo básico de um servidor Node.js com TypeScript;
- [`exemplo-dois`](./exemplo-dois): exemplo básico de um servidor Node.js.


### 📂 Estrutura da pasta `server/`
```
server/
├── exemplo-um/
│   ├── src/
│   ├── Dockerfile
│   └── ...
├── exemplo-dois/
│   ├── src/
│   ├── Falta codificar o Dockerfile
│   └── ...
└── README.md 
```


### 📁 Pré-requisitos

Antes de começar, você deve ter instalado em sua máquina:

- [Docker](https://www.docker.com/)

Para verificar utilize:
```bash
docker -v
```


### 🚀 Como executar o projeto

Clonando o repositório:
```bash
git clone https://github.com/arleysouza/introducao-docker.git server
cd server
```


### 📦 Exemplo 1: Aplicação Node.js com TypeScript

criação da imagem e container.
```bash
cd exemplo-um
docker build -t imagem-exemplo1:1.0.0 .
docker run -d --name container-exemplo1 -p 3011:3010 imagem-exemplo1:1.0.0
```


### 📦 Exemplo 2: Aplicação Node.js simples
Antes de prosseguir é necesário criar os arquivos `Dockerfile` e `.dockerignore`.
```bash
cd exemplo-dois
docker build -t imagem-exemplo2:1.0.0 .
docker run -d --name container-exemplo2 -p 3011:3010 imagem-exemplo2:1.0.0
```