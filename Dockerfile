FROM python:3.14

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "car"]
