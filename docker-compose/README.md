## Docker Compose com múltiplos serviços

Este diretório contém os arquivos e configurações utilizados na aula de Docker Compose, com o objetivo de integrar diferentes serviços em um ambiente unificado utilizando o `docker-compose.yml`.

Os serviços incluídos nesta aula são:
- PostgreSQL: banco de dados relacional;
- Back-end: servidor Node.js com Express;
- Front-end (dois projetos) – aplicações React com TypeScript.

### 📂 Estrutura da pasta `app/`
```
app/
├── adminer/
│   └── index.html
├── backend/
│   ├── src/
│   └── Dockerfile
├── db/
│   └── init.sql
├── front-um/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── Dockerfile
├── front-dois/
│   ├── public/
│   ├── src/
│   ├── vite.config.ts
│   └── Dockerfile
├── .dockerignore
├── compose.yml
└── README.md
```


### 📁 Pré-requisitos

Antes de iniciar, certifique-se de ter o Docker e o Docker Compose instalados:

```bash
docker -v
docker compose version
```


### 🚀 Como executar o ambiente

1. Clone o repositório e acesse a pasta:
```bash
git clone https://github.com/arleysouza/docker-compose.git app
cd app
```

2. Execute os serviços com Docker Compose:
```bash
docker compose up --build
```
Este comando construirá as imagens e iniciará todos os containers definidos no `compose.yml`.

3. Acesse os serviços no navegador:
- Servidor: http://localhost:3001/api 
- Front-end um: http://localhost:3002
- Front-end dois: http://localhost:3003
O PostgreSQL estará disponível em `localhost:5433`.

### 📦 Comandos úteis

Listar os containers em execução:
```bash
docker ps
```

Parar os serviços:
```bash
docker compose down
```

### 📌 Observações

- Os arquivos Dockerfile das aplicações front-end utilizam Vite, portanto, é necessário garantir que o `vite.config.ts` esteja configurado para permitir conexões externas
- O banco de dados PostgreSQL é inicializado com o script `init.sql` contido na pasta `db/`.