FROM python:3.11-slim
WORKDIR /app
COPY streaming/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY streaming /app/streaming
CMD ["python", "-m", "streaming.kafka_to_clickhouse"]
