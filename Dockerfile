FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /l_app

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

WORKDIR /l_app/src

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]