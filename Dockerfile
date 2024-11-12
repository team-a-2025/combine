# # ベースイメージとしてPythonを使用
# FROM python:3.9

# # 作業ディレクトリを設定
# WORKDIR /app

# # 必要なパッケージをインストール
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# # アプリケーションのソースコードをコピー
# COPY . .

# # Flaskアプリケーションを起動
# CMD ["python", "app.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--reload"]


# ベースイメージとしてPythonを使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数を設定
ENV FLASK_APP=app.py

# Flaskアプリケーションを起動
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
