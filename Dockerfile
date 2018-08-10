FROM python:3.7

COPY ./requirements.txt /service/requirements.txt

COPY ./app.py /service/app.py

RUN mkdir -p /data/service_logs

COPY ./project /service/project

COPY ./configs /service/configs

WORKDIR service

RUN pip install -r requirements.txt

EXPOSE 9002

CMD python app.py
