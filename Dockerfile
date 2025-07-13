FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl dos2unix && apt-get clean
RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache .

COPY start.sh .
RUN dos2unix start.sh && chmod +x start.sh

COPY src/ src/
COPY data.csv .

CMD ["./start.sh"]
