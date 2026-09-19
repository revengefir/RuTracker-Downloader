FROM python:3.12-slim
WORKDIR /app
ENV BOT_TOKEN = BOT_TOKEN
ENV USENAME = RutrackerUsername
ENV PASSWORD = RutrackerPassword

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "script.py"]
