FROM nginx:1.27-alpine
COPY frontend/ /usr/share/nginx/html/
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
HEALTHCHECK --interval=15s --timeout=5s --retries=5 CMD wget --spider -q http://localhost/ || exit 1
