import sqlite3
import os, json
from typing import Any
from pathlib import Path

def search_db(table: str, condition: str) -> int:
    # 현재 파일 기준 절대 경로
    BASE_DIR = Path(__file__).resolve().parent
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'sns.db'))
    cursor = conn.cursor()

    create_sql = f'SELECT * FROM {table} WHERE {condition}'
    cursor.execute(create_sql)

    result = cursor.fetchall()
    conn.close()

    return len(result)