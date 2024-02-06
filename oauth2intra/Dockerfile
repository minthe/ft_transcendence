FROM python:3.12.1-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . .

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# RUN python manage.py makemigrations
# RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]