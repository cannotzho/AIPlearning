FROM python:3.10.11-slim AS builder

COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gfortran libopenblas-dev && \
    rm -rf /var/lib/apt/lists/* &&\
    pip install --user --no-cache-dir -r requirements.txt &&\
    find /root/.local \
    \( -type d -name test -o -name tests \) -prune -o \
    \( -type f -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' +

FROM python:3.10.11-slim

WORKDIR /app

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 &&\
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local

COPY . .

ENV PATH="/root/.local/bin:$PATH"

CMD ["python", "app.py"]
