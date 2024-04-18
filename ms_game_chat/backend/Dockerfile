FROM python:3.12.1-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG DEBUG
ENV DEBUG=${DEBUG}

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . .

# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:6969"]
# CMD ["sh", "-c", "python manage.py makemigrations; python manage.py migrate; daphne -b 0.0.0.0 -p 6969 backend.asgi:application"]
CMD ["./ms_game_chat_start.sh"]