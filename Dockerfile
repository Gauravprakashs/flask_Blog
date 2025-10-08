FROM python:3.11

WORKDIR /app

COPY . /app
COPY entrypoint.sh /app/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

CMD ["/app/entrypoint.sh"]