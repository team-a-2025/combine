from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# MySQLの接続設定
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='db',
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# ログイン画面のルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # ここでMySQLからユーザーを認証する処理
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            return redirect(url_for('todo'))
        else:
            error = '無効なユーザー名またはパスワード'
    return render_template('login.html', error=error)

# タスク入力画面のルート
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = request.form['content']
        # MySQLにタスクを保存する処理を追加
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tasks (content) VALUES (%s)', (task,))
        connection.commit()
        connection.close()
        return render_template('todo.html', task=task)
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
