FROM python:3.11-slim

RUN apt-get -y update && \
apt-get -y install curl && \
apt-get install sudo

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

#Debian 12
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

RUN sudo apt-get -y install gnupg
#RUN sudo apt-key adv --fetch-keys http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xEB3E94ADBE1229CF

RUN mkdir -p /etc/apt/keyrings \
    # Add Microsoft key to keyring
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg \
    # Download appropriate package for the OS version (currently Debian 12)
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update
#RUN apt-get clean
RUN sudo apt-get update
RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN sudo apt-get install -y unixodbc-dev

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./packages ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./app ./app

RUN poetry install --no-interaction --no-ansi

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
