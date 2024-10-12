FROM python:3.11-slim
WORKDIR /code
RUN pip install kafka-python stripe
COPY outward_sync.py .
CMD ["python3", "outward_sync.py"]
