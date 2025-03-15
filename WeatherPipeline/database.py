from flask import Flask, request, render_template, jsonify
import sqlite3
from datetime import datetime
import pandas as pd
import psycopg2

# Initializing 
app = Flask(__name__)

def init_sqlite_db():
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

def connect_postgresql_db():
    # Nawiązanie połączenia z bazą danych
    conn = psycopg2.connect(
        database="my_test",  # Nazwa bazy danych (musi istnieć!)
        user="newuser",           # Nazwa użytkownika PostgreSQL
        password="password",      # Hasło użytkownika
        host="localhost",         # Adres serwera (np. localhost lub IP)
        port="5432"               # Standardowy port PostgreSQL to 5432 (5001 to raczej błąd!)
    )

    return conn

def get_sqlite_log_by_id(log_id):
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    
    sql = "SELECT * FROM requests_log WHERE id = ?"
    cursor.execute(sql, (log_id,))
    
    log = cursor.fetchone()
    conn.close()

    return log

def get_psql_log_by_id(log_id):
    conn = connect_postgresql_db()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM requests_log WHERE id = %s;"
    cursor.execute(sql, (log_id,))
    
    log = cursor.fetchone()
    conn.close()

    return log



# Error Handling
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Wystąpił błąd serwera"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Nie znaleziono strony"}), 404



# Domains 
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
    sql_lite = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (?, ?, ?, ?)"
    psql = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (%s, %s, %s, %s);"

    # Updating SQLite DB
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    cursor.execute(sql_lite, (ip, user_agent, request_time, domain))
    conn.commit()
    conn.close()

    # Updating Postgresql DB
    psqlconn = connect_postgresql_db()
    if psqlconn:
        cur = psqlconn.cursor()
        cur.execute(psql, (ip, user_agent, request_time, domain))
        psqlconn.commit()
        cur.close()
        psqlconn.close()
    else:
        print("Nie udało się połączyć z PostgreSQL")
    return "/home"

@app.route('/test')
def test():
    ip = request.host
    user_agent = request.headers.get("User-Agent")
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain = "/test"
    sql_lite = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (?, ?, ?, ?)"
    psql = "INSERT INTO requests_log (ip, user_agent, request_time, domain) VALUES (%s, %s, %s, %s);"

    # Updating SQLite DB
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    cursor.execute(sql_lite, (ip, user_agent, request_time, domain))
    conn.commit()
    conn.close()

    # Updating Postgresql DB
    psqlconn = connect_postgresql_db()
    if psqlconn:
        cur = psqlconn.cursor()
        cur.execute(psql, (ip, user_agent, request_time, domain))
        psqlconn.commit()
        cur.close()
        psqlconn.close()
    else:
        print("Nie udało się połączyć z PostgreSQL")
    return "/test"

@app.route('/sqlite_logs')
def sqlite_logs():

    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM requests_log"
    cursor.execute(sql)
    # df = pd.read_sql_query('SELECT * FROM requests_log ORDER BY request_time DESC', conn)
    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)

@app.route('/psql_logs')
def psql_logs():
    try:
        conn = connect_postgresql_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM requests_log"
        cursor.execute(sql)
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Błąd podczas łączenia z bazą danych: {e}")

    return render_template("logs.html", logs=logs)

@app.route('/sqlite_logs/<int:log_id>', methods=['GET'])
def get_log_sqlite(log_id):
    log = get_sqlite_log_by_id(log_id)
    
    if log is None:
        return jsonify({"error": "Log o podanym ID nie istnieje"}), 404
    
    log_data = {
        "id": log[0],
        "method": log[1],  
        "url": log[2],
        "status_code": log[3],
        "request_time": log[4]
    }
    return jsonify(log_data)

@app.route('/psql_logs/<int:log_id>', methods=['GET'])
def get_log_psql(log_id):
    log = get_psql_log_by_id(log_id)
    
    if log is None:
        return jsonify({"error": "Log o podanym ID nie istnieje"}), 404
    
    log_data = {
        "id": log[0],
        "method": log[1],  
        "url": log[2],
        "status_code": log[3],
        "request_time": log[4]
    }
    return jsonify(log_data)



# Initializing dbs
init_sqlite_db()
connect_postgresql_db()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
