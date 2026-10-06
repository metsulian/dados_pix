FROM postgres:16

ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-db.txt .
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements-db.txt

COPY src ./src

COPY load_data.sh /docker-entrypoint-initdb.d/10-load_data.sh
RUN chmod +x /docker-entrypoint-initdb.d/10-load_data.sh