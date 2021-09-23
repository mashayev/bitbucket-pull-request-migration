FROM python:3.7

RUN pip install PyGithub click

ADD src/migrate.py .
