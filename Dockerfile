FROM python:3.11
WORKDIR /code
COPY ./app /code/app
COPY main.py /code/main.py
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["fastapi", "run", "main.py", "--port", "80"]
