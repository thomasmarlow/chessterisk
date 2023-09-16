FROM python:3.9-slim AS pepe
WORKDIR /app
COPY . .
RUN chmod +x /app/docker-entrypoint.sh
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/app/docker-entrypoint.sh"]
