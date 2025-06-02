# Stage 1: Build the React app.
FROM node:22.16.0-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY public/ ./public
COPY src/ ./src
ENV REACT_APP_API_URL=http://robot-service.local
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:1.27.5-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80 # Expose the application port. Not required for Kubernetes pod containers.
CMD ["nginx", "-g", "daemon off;"]
