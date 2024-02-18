FROM registry.redhat.io/ubi8/python-36

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python /app/init_db.py && flask run"]~
