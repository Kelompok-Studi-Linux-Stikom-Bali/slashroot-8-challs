FROM python:alpine

RUN apk add --no-cache socat
RUN pip install pycryptodome
COPY chall.py /chall.py

CMD socat TCP-LISTEN:13337,fork,reuseaddr EXEC:"python3 /chall.py"
