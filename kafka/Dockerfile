FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir kafka-python==2.0.2
COPY kafka/simulator.py /app/simulator.py
CMD ["python", "/app/simulator.py"]
