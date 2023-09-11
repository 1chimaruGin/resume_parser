# FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime
FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

RUN export DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Add Miniconda to PATH
ENV PATH /opt/conda/bin:$PATH

# Optionally, create a base environment or install default packages
RUN conda update -n base conda && \
    conda clean -afy

RUN pip install uvicorn gunicorn poetry
# RUN pip install poetry
# # ADD pyproject.toml poetry.lock /code/

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app /app
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app/
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10
RUN poetry install --no-root

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]