import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


connection_string = os.environ.get('POSTGRES_CONNECTION_STRING')

conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}

conn_string = "host={0} user={1} dbname={2} password={3} sslmode=require".format(
    conn_str_params['host'],
    conn_str_params['user'],
    conn_str_params['dbname'],
    conn_str_params['password'])


def get_db_connection():
    """To connect to the Postgres database

    Returns:
        _type_: _description_
    """
    conn = psycopg2.connect(connection_string)
    return conn



@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')