-- CREATE TABLE IF NOT EXISTS tasks (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     description TEXT,
--     completed BOOLEAN NOT NULL DEFAULT FALSE
-- );
-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(255) NOT NULL,
--     password VARCHAR(255) NOT NULL
-- );


CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- テスト用ユーザーの追加（パスワードは'password123'をハッシュ化したもの）
INSERT INTO users (username, password) VALUES (
    'admin',
    '$pbkdf2-sha256$29000$eVYl6OwySzcHSl/4Cm6NJA$6ieJ/dkZkOB1jlXsoXo9/UMpUNx1ALOWIh1kcwDjYx8'
);
