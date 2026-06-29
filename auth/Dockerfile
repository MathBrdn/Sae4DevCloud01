FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . /workspace/
EXPOSE 8001
CMD ["gunicorn", "--chdir", "/workspace", "auth.wsgi:application", "--bind", "0.0.0.0:8001"]

