# Estágio 1: Build
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Produção (Nginx)
FROM nginx:alpine
# Copia os arquivos gerados no build para a pasta do Nginx
COPY --from=build /app/dist /usr/share/nginx/html
# Configuração padrão do Nginx (opcional, mas recomendada para React Router)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]