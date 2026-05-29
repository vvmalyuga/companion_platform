FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir feast==0.45.0 redis==5.2.1 pandas==2.2.3 pyarrow==18.1.0
COPY feast/companion_platform /app/companion_platform
WORKDIR /app/companion_platform
CMD ["python", "materialize_and_retrieve.py"]
