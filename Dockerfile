# Use an official Python runtime as the base image
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1


# Set the working directory in the container
WORKDIR /app

# Add Aliyun's APT sources
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@security.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the local application files to the container
COPY . /app

# Install Python dependencies
# Generate requirements.txt if not already present
RUN if [ ! -f requirements.txt ]; then \
        pip install --no-cache-dir pipreqs && \
        pipreqs /app --force; \
    fi

# Use Aliyun's PyPI mirror for faster installation
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt

# Expose a port if necessary (adjust the port number based on your app)
EXPOSE 5000

# Run the application (adjust as needed)
CMD python run.py
