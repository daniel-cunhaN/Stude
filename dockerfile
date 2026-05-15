FROM python:3.11.15-slim

WORKDIR /pastadocker

COPY dependencias.txt . 
RUN pip install -r dependencias.txt
COPY . .

EXPOSE 8501