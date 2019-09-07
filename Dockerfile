FROM alpine:3.10
MAINTAINER Lennart Weller <lhw@ring0.de>

COPY . /app/
WORKDIR /app
RUN apk add --no-cache python3 py3-pip\
    && pip3 install -r requirements.txt

USER guest

ENTRYPOINT ["python3", "main.py"]
