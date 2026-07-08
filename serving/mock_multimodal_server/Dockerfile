FROM python:3.11-slim
WORKDIR /app
COPY serving/mock_multimodal_server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY serving/mock_multimodal_server/server.py /app/server.py
EXPOSE 8001
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]

