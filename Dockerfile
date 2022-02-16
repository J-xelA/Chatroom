FROM python:3.6-stretch
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
COPY requirements.txt ./
RUN pip3 install --user -r requirements.txt
COPY . app
COPY run_server.sh ./
RUN chmod +x run_server.sh
EXPOSE 8000
ENTRYPOINT ["./run_server.sh"]
