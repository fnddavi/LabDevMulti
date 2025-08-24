# Etapa 1: build da aplicação
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Etapa 2: servir com um servidor estático (usando nginx)
FROM nginx:alpine

# Copia arquivos gerados no build para o nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Expor a porta padrão do nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
