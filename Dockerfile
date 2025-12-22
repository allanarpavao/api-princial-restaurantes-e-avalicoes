FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Linha 6: Expõe a porta (documenta qual porta sua API usa)
EXPOSE 8000

CMD ["python", "app.py"]
