FROM registry.redhat.io/ubi8/python-36
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD templates /app/templates
COPY app.py /app
CMD ["flask", "run"]~
