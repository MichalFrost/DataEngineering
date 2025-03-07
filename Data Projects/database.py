from flask import Flask, request, render_template
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)

def init_db():
    conn =  sqlite3.connect("requests.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests_log (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ip TEXT,
                   user_agent TEXT,
                   request_time TEXT,
                   domain TEXT)
                   """)
    conn.commit()
    conn.close()

@app.route('/')
def hello_world():
    print(request.headers)
    return "Hello World!"

@app.route('/home')
def home():
    ip = request.host
    user_agent = request.headers.get("User-Agent")
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain = "/home"

    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    sql = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (ip, user_agent, request_time, domain))

    conn.commit()
    conn.close()
    return "/home"

@app.route('/test')
def test():
    ip = request.host
    user_agent = request.headers.get("User-Agent")
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain = "/test"

    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    sql = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (ip, user_agent, request_time, domain))

    conn.commit()
    conn.close()
    return "/test"

@app.route('/logs')
def logs():

    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM requests_log"
    cursor.execute(sql)

    df = pd.read_sql_query('SELECT * FROM requests_log ORDER BY request_time DESC', conn)
    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)


init_db()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)