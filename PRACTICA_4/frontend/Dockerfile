# ---- Etapa 1: build del frontend con Node ----
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---- Etapa 2: servir los archivos estáticos con nginx ----
FROM nginx:1.27-alpine

# Configuración de nginx (sirve la SPA y hace proxy de /api hacia el backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar el build generado en la etapa anterior
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
