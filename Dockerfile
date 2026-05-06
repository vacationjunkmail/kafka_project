FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# To keep container up after starting the container
RUN ls -R /app
CMD ["python", "kafka_app/kafka_app/main.py", "-t", "Dana1", "-c"]

