FROM python:3.7-alpine
MAINTAINER Lennart Weller <lhw@ring0.de>

COPY . /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

USER guest

ENTRYPOINT ["python3", "main.py"]
