from tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && apt-get install curl git -y
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

RUN mkdir -p /app/ac-backend/
WORKDIR /app/ac-backend/
COPY ./ .


RUN poetry install
