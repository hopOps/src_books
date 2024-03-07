FROM registry.redhat.io/ubi9/python-39

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["sh", "-c", "flask run"]~
