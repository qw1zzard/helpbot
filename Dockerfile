FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache .

COPY src/ src/
COPY start.sh .
COPY data.csv .

RUN chmod +x start.sh
CMD ["./start.sh"]
