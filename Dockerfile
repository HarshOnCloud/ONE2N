FROM python:3.9-slim

WORKDIR /app

COPY metrics_collection.py .

RUN pip install requests kubernetes

CMD ["python", "metrics_collection.py"]