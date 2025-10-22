FROM python:3.10.11-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gfortran libopenblas-dev && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.10.11-slim

COPY ./requirements.txt .

RUN python -m venv /opt/venv &&\
    . /opt/venv/bin/activate &&\
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "app.py"]
