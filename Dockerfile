FROM alpine/flake8:latest

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["sh", "-c", "flask run"]~
