FROM python:3.10-slim
WORKDIR /app
COPY backend ./backend
COPY frontend ./frontend
WORKDIR /app/backend
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
