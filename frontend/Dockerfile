# Multi-stage build per school-project-conventions: full node toolchain only
# in the build stage, slim runtime image shipped.

FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
# Runs as non-root, per school-project-conventions.
RUN addgroup -S app && adduser -S app -G app \
    && chown -R app:app /var/cache/nginx /var/run /var/log/nginx
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.static.conf /etc/nginx/conf.d/default.conf
USER app
EXPOSE 8080
