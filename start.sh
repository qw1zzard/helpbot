#!/bin/bash

uvicorn src.main:app --host localhost --port 80 &

until curl -s http://localhost:80/ > /dev/null; do
    sleep 1
done

streamlit run src/ui/app.py --server.port 8501
python src/telegram/bot.py
