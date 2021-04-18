FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y libmysqlclient-dev && \
    apt-get clean
WORKDIR /project1
ADD . /project1
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["gunicorn", "board.wsgi:application", "--bind", "0.0.0.0:8000"]