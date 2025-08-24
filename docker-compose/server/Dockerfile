#### Etapa 1: Build da aplicação

# Usa uma imagem base leve com Node.js
FROM node:20-alpine AS builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências (package.json e package-lock.json) e compilar o TypeScript
COPY package*.json tsconfig.json ./

# Copia o código-fonte TypeScript para dentro do container
COPY src ./src

# Instala todas as dependências, incluindo as de desenvolvimento
RUN npm install

# Compila o código TypeScript, gerando os arquivos JavaScript em /app/dist
RUN npm run build


#### Etapa 2: Execução da aplicação

# Usa novamente uma imagem leve para execução em produção
FROM node:20-alpine AS production

# Define o diretório de trabalho no container final
WORKDIR /app

# Copia os arquivos compilados da etapa de build
COPY --from=builder /app/dist ./dist

# Copia os arquivos de definição de dependências
COPY --from=builder /app/package*.json ./

# Copia a pasta node_modules da etapa de build
COPY --from=builder /app/node_modules ./node_modules

# Define a variável de ambiente para indicar o modo de produção
# Indica que o ambiente de execução da aplicação Node.js é o de produção
ENV NODE_ENV=production

# Comando padrão ao iniciar o container
CMD ["node", "dist/index.js"]
