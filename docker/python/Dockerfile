FROM python:3.10

RUN pip install --upgrade pip setuptools==68.2.2

COPY ./student_infobase /srv/www/student_infobase
WORKDIR /srv/www/student_infobase

RUN pip install -r requirements.txt