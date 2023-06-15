FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
COPY diploma-frontend frontend

RUN pip install --upgrade pip
RUN pip install frontend/dist/diploma-frontend-0.6.tar.gz
RUN pip install -r requirements.txt

COPY megano megano

RUN python3 megano/manage.py migrate