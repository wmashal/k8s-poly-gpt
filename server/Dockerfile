# Use a slimmer base image
FROM --platform=linux/amd64 python:3.11-slim AS builder

# Environment variables
ENV OPENAI_API_KEY=""
ENV ATOMCONFIG=""
ENV GOPRIVATE=""
ENV GIT_TERMINAL_PROMPT=1

# Arguments for user and group IDs
ARG UID=1000
ARG GID=1000

# Set working directory
WORKDIR /app

# Create a non-root user and switch to it
RUN groupadd --gid $GID appuser && useradd --uid $UID --gid $GID -m appuser

# Install Python dependencies (combining into a single RUN)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install llama-index \
    && pip install chromadb \
    && pip install llama-index-vector-stores-chroma

# Copy source code and documents
COPY EXTRA_COMMANDS ./EXTRA_COMMANDS

# Install system dependencies (only what's necessary)
RUN apt-get update && apt-get install -y --no-install-recommends curl git build-essential wget tar sudo git vim-tiny g++-x86-64-linux-gnu libc6-dev-amd64-cross \
    && rm -rf /var/lib/apt/lists/* # Clean up

# Download and install GPTscript (combining into a single RUN)
RUN curl -s https://api.github.com/repos/gptscript-ai/gptscript/releases/latest \
    | grep "browser_download_url.*-linux-amd64.tar.gz" \
    | cut -d '"' -f 4 \
    | xargs curl -LO \
    && tar -xzf *.tar.gz -C /usr/local/bin \
    && rm *.tar.gz


# TODO (optional): Install additional tools or dependencies

# Install kubectl (run as root, then switch back)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
#USER appuser

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
