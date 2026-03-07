nano DockerfileFROM python:3.14-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "src/__main__.py"]
