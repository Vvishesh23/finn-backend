FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock
COPY backend/app backend/app
COPY frontend frontend
COPY demo demo
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "python -m uvicorn backend.app.main:app --no-proxy-headers --no-access-log --workers 1 --host 0.0.0.0 --port ${PORT:-8000}"]
