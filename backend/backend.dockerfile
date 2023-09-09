FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# FROM mambaorg/micromamba:1.4.1-bullseye-slim

WORKDIR /app/

# Install Poetry
RUN pip install poetry
# ADD pyproject.toml poetry.lock /code/
COPY ./app/pyproject.toml ./app/poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10
RUN poetry install --no-root

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /app
ENV PYTHONPATH=/app
