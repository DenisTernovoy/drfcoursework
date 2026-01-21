FROM python:3.14

WORKDIR drf/

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry", "run"]
