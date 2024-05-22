FROM python:3.9

COPY vault.py .
COPY .env .

RUN pip install hvac \
    python-dotenv

CMD ["python", "vault.py"]