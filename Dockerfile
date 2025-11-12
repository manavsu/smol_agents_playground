FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install the uv CLI so the script headers in `main.py` can be honored.
RUN pip install --no-cache-dir uv

# Ship the project files. uv will install requirements when the container starts.
COPY . .

CMD ["uv", "run", "--script", "main.py"]
