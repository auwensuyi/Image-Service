FROM python:3.9-slim-buster

WORKDIR /app

COPY app.py /app/
COPY service /app/service
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]