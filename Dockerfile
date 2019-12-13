FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python3-dev build-essential


COPY requirements.txt requirements.txt

COPY app app
COPY migrations migrations
COPY config.py app.py app.db ./

WORKDIR ./

RUN pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["python"]

CMD ["app.py"]
