import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 設定 Log 檔案名稱
log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# 設定 Logging
log_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7, encoding="utf-8")
log_handler.setLevel(logging.INFO)  # 記錄 INFO 以上的訊息
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

# 設定 Logger（讓 Flask 也能使用這個 Logger）
logger = logging.getLogger("flask_logger")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)