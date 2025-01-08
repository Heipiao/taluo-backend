# Use an official Python runtime as the base image
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

# Set the working directory in the container
WORKDIR /app

# Configure Aliyun yum repository and install additional system utilities
RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
    yum makecache && \
    yum update -y && \
    yum install -y \
    ps \
    vim \
    && yum clean all

# Copy the local application files to the container
COPY . /app

# Use Aliyun's PyPI mirror for faster installation
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt

# Expose a port if necessary (adjust the port number based on your app)
EXPOSE 5000

# Run the application (adjust as needed)
CMD python src/run.py
