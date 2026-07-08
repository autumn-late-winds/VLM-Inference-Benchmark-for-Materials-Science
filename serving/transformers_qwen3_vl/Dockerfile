FROM python:3.11-slim
WORKDIR /app
COPY serving/transformers_qwen3_vl/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY serving/transformers_qwen3_vl/server.py /app/server.py
EXPOSE 8002
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8002"]

