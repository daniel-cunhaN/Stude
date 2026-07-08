FROM python:3.11-slim

WORKDIR /app

COPY requisitos.txt .

RUN pip install --no-cache-dir -r requisitos.txt

# Copy the rest of the application
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
