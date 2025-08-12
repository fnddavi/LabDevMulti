# Etapa 1: Imagem final para produção
# Usa uma imagem base leve com Node.js v20 (Alpine é uma distribuição enxuta)
FROM node:20-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de manifesto de pacotes para aproveitar o cache do Docker
COPY package*.json ./

# Copia o arquivo .env com as variáveis de ambiente
COPY .env ./

# Instala apenas as dependências essenciais para execução
# O comando --omit=dev garante que pacotes de desenvolvimento não sejam instalados
RUN npm install --omit=dev

# Copia o código-fonte da aplicação
COPY src ./src

# Expõe a porta definida no .env ou o padrão 3000 (ajuste se necessário)
EXPOSE 3012

# Define o comando que será executado ao iniciar o container
CMD ["node", "src/index.js"]