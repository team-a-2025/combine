from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理用のシークレットキー

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
        print(f"Database connection error: {err}")
        return None

# ユーザー登録のルート（ハッシュ化されたパスワードで登録）
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # パスワードをハッシュ化してデータベースに保存
        hashed_password = generate_password_hash(password)
        
        try:
            connection = get_db_connection()
            if connection is None:
                error = 'データベース接続に失敗しました'
                return render_template('register.html', error=error)
            
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            connection.commit()
            connection.close()
            flash('登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
        
        except mysql.connector.Error as db_err:
            error = 'データベースエラーが発生しました'
            print(f"Database error: {db_err}")

    return render_template('register.html', error=error)

# ログイン画面のルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            if connection is None:
                error = 'データベース接続に失敗しました'
                return render_template('login.html', error=error)

            cursor = connection.cursor()
            cursor.execute('SELECT password FROM users WHERE username=%s', (username,))
            user = cursor.fetchone()
            connection.close()

            if user and check_password_hash(user[0], password):
                session['username'] = username  # セッションにユーザー名を保存
                return redirect(url_for('todo'))  # 認証成功時にTodo入力画面にリダイレクト
            else:
                error = '無効なユーザー名またはパスワード'
        
        except mysql.connector.Error as db_err:
            error = 'データベース処理中にエラーが発生しました'
            print(f"Database error: {db_err}")  # ターミナルにエラーログを出力

    return render_template('login.html', error=error)

# Todo入力画面のルート
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    # セッションにユーザー名がない場合は、ログイン画面にリダイレクト
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # タスクをデータベースに保存する処理（必要に応じて追加可能）
        # ここでは、追加されたタスク情報をテンプレートに渡して表示
        return render_template('todo.html', title=title, description=description)
    
    return render_template('todo.html')

# ログアウトのルート
@app.route('/logout')
def logout():
    session.pop('username', None)  # セッションからユーザー情報を削除
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
