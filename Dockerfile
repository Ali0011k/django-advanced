FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py makemigrations --noinput &&\   
    python manage.py migrate --noinput&&\
    python manage.py createsuperuser --email $EMAIL --noinput;\
    python manage.py runserver 0.0.0.0:8000
