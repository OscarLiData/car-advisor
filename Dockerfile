FROM python:3.14

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "car"]
