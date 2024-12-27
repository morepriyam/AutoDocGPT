FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    git && \
    apt-get clean

# Set up Python virtual environment
RUN python3 -m venv /venv

# Set working directory
WORKDIR /app

# Install Python packages
COPY requirements.txt /app/requirements.txt
RUN /venv/bin/pip install -r requirements.txt

# Copy necessary scripts
COPY entrypoint.sh /entrypoint.sh
COPY generate_readme.py /generate_readme.py

ENTRYPOINT ["/entrypoint.sh"]
