FROM python:3.11-slim
WORKDIR /code
RUN pip install kafka-python stripe schedule sqlalchemy psycopg2-binary
COPY inward_sync.py .
CMD ["python3", "inward_sync.py"]
