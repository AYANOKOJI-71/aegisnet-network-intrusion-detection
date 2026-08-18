FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY apps/api/src ./apps/api/src
RUN pip install --no-cache-dir .

EXPOSE 4500
CMD ["uvicorn", "aegisnet.app:app", "--host", "0.0.0.0", "--port", "4500"]
