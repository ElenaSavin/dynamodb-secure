FROM python:3.9

ADD . /

RUN pip3 install -r ./requirements.txt

ENV FLASK_APP=app.py 

ARG ["printenv"]
CMD [ "python3", "app/app.py" ]
