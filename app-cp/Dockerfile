FROM bitnami/python
LABEL maintainer "Nabil Servais <nabil.servais@gmail.com>"

WORKDIR /opt/api-codepostaux/

COPY app.py import.py requirements.txt mysql2redis.py ./
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "-b", "0.0.0.0"]
