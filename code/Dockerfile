FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
        clang \
        llvm \
        llvm-dev \
        clang-format \
        clang-tidy \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /compiler

COPY requirements.txt /compiler/
RUN pip install -r requirements.txt


CMD ["/bin/sh"]
# FROM python:3-alpine3.20



# RUN apk update && \
#     apk add --no-cache \
#     llvm15 \
#     llvm15-libs \
#     llvm15-dev \
#     llvm15-static

# # Verify the installation
# RUN llvm-config --version

# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# COPY /compiler /app

# RUN pip install -r requirements.txt


# CMD ["/bin/sh"]
