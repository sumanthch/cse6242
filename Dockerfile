# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

FROM tiangolo/uvicorn-gunicorn:python3.9

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the source code into the container.
COPY ./models /code/models
COPY ./main.py /code/main.py

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
