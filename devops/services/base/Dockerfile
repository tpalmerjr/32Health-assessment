FROM python:3.11.5-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./devops/services/base/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./devops/services/base/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

WORKDIR /app

# Requirements are installed here to ensure they will be cached.
COPY ./services/${SERVICE_NAME}/Pipfile ./services/${SERVICE_NAME}/Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --deploy --system

ENTRYPOINT ["/entrypoint.sh"]
