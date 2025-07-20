FROM python:3.13-slim-bookworm

WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y curl dos2unix && apt-get clean
RUN pip install -U pip && pip install uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache .

COPY start.sh .
RUN dos2unix start.sh && chmod +x start.sh

COPY src/ src/
COPY prompts/ prompts/
COPY data/data.csv .

CMD ["./start.sh"]
