FROM python:3.11-alpine
RUN adduser -s /usr/sbin/nologin -u 1001 -D app
USER app

WORKDIR /app
COPY --chown=app:app . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "main.py"]