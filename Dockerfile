FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

RUN chmod +x entrypoint.sh
CMD ./entrypoint.sh

EXPOSE 8000