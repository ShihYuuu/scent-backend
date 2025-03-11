import os
import pymysql
import datetime
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from db import get_db_connection
from dotenv import load_dotenv

from logging.handlers import TimedRotatingFileHandler

load_dotenv()

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config["DEBUG"] = True

# 設定 JWT 秘密金鑰
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")
jwt = JWTManager(app)

CORS(app) 

# LOGS
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log")

# 設定 Logging
log_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7, encoding="utf-8")
log_handler.setLevel(logging.INFO)  # 記錄 INFO 以上的請求
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

# 設定 Flask Logger
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# 記錄所有 POST 請求（包含時間、IP、URL、請求 Body）
@app.before_request
def log_post_requests():
    if request.method == "POST":
        log_data = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "method": request.method,
            "url": request.path,
            "headers": dict(request.headers),
            "body": request.get_json(silent=True),  # 避免非 JSON 請求報錯
        }
        app.logger.info(f"POST request: {log_data}")

# 記錄所有錯誤
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error: {e}", exc_info=True)
    return jsonify({"error": "Internal Server Error"}), 500

# 測試 API（模擬 POST）
@app.route("/api/test", methods=["POST"])
def test_post():
    data = request.get_json()
    return jsonify({"message": "Received", "data": data}), 200

@app.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cursor: 
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall() 

    conn.close()
    return jsonify(users)

@app.route("/api/add_user", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data["name"], data["email"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully!"})

@app.route("/api/login", methods=["POST"])
def login():
    # 解析前端傳來的 JSON
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # 檢查 email 和 password 是否存在
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    # 連接 MySQL
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            # 查詢使用者資料
            sql = "SELECT id, name, password FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

        # 如果使用者不存在
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # 檢查密碼是否正確（假設密碼是純文字，未加密）
        stored_password = user["password"]  # ⚠️ 這裡應該使用 Hash 儲存密碼
        if password != stored_password:
            return jsonify({"error": "Invalid email or password"}), 401

        # 產生 JWT Token（有效時間 1 小時）
        access_token = create_access_token(
            identity={"id": user["id"], "name": user["name"], "email": email},
            expires_delta=datetime.timedelta(hours=1)
        )

        return jsonify({"message": "Login successful", "token": access_token})

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=8000)