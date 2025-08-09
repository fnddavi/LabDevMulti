#### Etapa 1: Construção da aplicação

# Usa uma imagem base leve com Node.js v20 (Alpine é uma distribuição enxuta)
FROM node:20-alpine AS builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessários para instalar as dependências e compilar o TypeScript
COPY package.json tsconfig.json ./

# Copia o código-fonte TypeScript
COPY src ./src

# Instala todas as dependências (inclusive as de desenvolvimento)
RUN npm install

# Compila o código TypeScript, gerando os arquivos JavaScript em /app/dist
RUN npm run build


#### Etapa 2: Imagem final para produção

# Usa a mesma imagem base leve, agora para a execução da aplicação
FROM node:20-alpine AS production

# Define novamente o diretório de trabalho no container final
WORKDIR /app

# Copia apenas o código compilado (JavaScript) da etapa de build
COPY --from=builder /app/dist ./dist

# Copia o package.json para instalar apenas as dependências de produção
COPY package.json ./

# Copia o arquivo .env com as variáveis de ambiente
COPY .env ./

# Instala apenas as dependências essenciais para execução
RUN npm install --omit=dev

# Expõe a porta 3011 do container (ajuste conforme o `process.env.PORT` do app)
EXPOSE 3011

# Define o comando que será executado ao iniciar o container
CMD ["node", "dist/index.js"]
