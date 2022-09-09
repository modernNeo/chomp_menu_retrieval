FROM python:3.9.13-alpine
RUN apk update && apk add alpine-conf
RUN setup-timezone -z Canada/Pacific

WORKDIR /src
COPY requirements.txt requirements.txt
COPY chomp.env chomp.env
COPY chomp.py chomp.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "chomp.py"]

#CMD ["sh"]
