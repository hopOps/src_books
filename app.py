import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)

def init_db():
    """Create Database schema

    Returns:
        None
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('books',))
    if cur.fetchone()[0]:
        print("DB OK")
    else:
        cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                        'title varchar (150) NOT NULL,'
                                        'author varchar (50) NOT NULL,'
                                        'pages_num integer NOT NULL,'
                                        'review text,'
                                        'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                        )
    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    """To connect to the Postgres database

    Returns:
        class: connect to db
    """
    conn_str = os.environ['POSTGRESQLCONNSTR_postgres_conn_string']
    conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode=require".format(
        conn_str_params['host'],
        conn_str_params['user'],
        conn_str_params['dbname'],
        conn_str_params['password'])
    conn = psycopg2.connect(conn_string)
    return conn


@app.route('/')
def index():
    init_db() # to change
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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
