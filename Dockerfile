FROM python:3.8-buster

RUN groupadd -r server && useradd -r -g server server

EXPOSE 8080
EXPOSE 443

RUN mkdir /niched

ADD requirements.txt /niched/

WORKDIR /niched

RUN pip3 install --no-cache-dir -r requirements.txt

ADD . /niched

RUN chown -R server:server /niched

USER server

CMD uvicorn --host 0.0.0.0 --port $PORT --workers 8 niched.main:app
