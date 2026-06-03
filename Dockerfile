FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nextflow (for pipeline orchestration)
RUN wget -qO- https://get.nextflow.io | bash && mv nextflow /usr/local/bin/

# Default workdir
COPY . /app
ENV PATH="/app:${PATH}"

CMD ["bash"]
