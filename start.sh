#!/bin/bash

uvicorn src.main:app --host localhost --port 80 &

until curl -s http://localhost:80/ > /dev/null; do
    sleep 1
done

streamlit run src/app/ui.py --server.port 8501
