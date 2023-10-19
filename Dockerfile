FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_PASSWORD=ali0013khani

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py makemigrations --noinput &&\   
    python manage.py migrate --noinput&&\
    python manage.py createsuperuser --email kly441781@gmail.com --noinput;\
    python manage.py runserver 0.0.0.0:8000