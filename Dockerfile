FROM --platform=linux/amd64 python:3.11

WORKDIR /code

# Install system dependencies for cadquery-ocp (OpenGL, X11 libraries)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libsm6 \
    libice6 \
    libxt6 \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]