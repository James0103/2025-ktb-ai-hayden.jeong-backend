# 가상의 DB 생성 파일
# SQLite를 이용한 간단한 DB 생성
import sqlite3
import os, json
from typing import Any

script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(script_dir, 'json_data')
DATA_FILES = ['posts.json', 'reply.json', 'user.json']

# DB파일 생성
conn = sqlite3.connect(os.path.join(DATA_PATH, 'sns.db'))
cursor = conn.cursor()

# 테이블 스키마 정의
TABLE_SCHEMA = {
    'user': {
        'columns': ['id', 'nickname', 'email', 'profile_image'],
        'types': ['TEXT PRIMARY KEY', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT']
    },
    'reply': {
        'columns': ['id', 'post_id', 'author', 'contents', 'last_upload_at'],
        'types': ['TEXT PRIMARY KEY', 'TEXT', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT']
    },
    'posts': {
        'columns': ['id', 'title', 'author', 'contents', 'like_count', 'reply_count', 'view_count', 'last_upload_at', 'img'],
        'types': ['TEXT PRIMARY KEY', 'TEXT', 'TEXT NOT NULL', 'TEXT NOT NULL', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT', 'TEXT']
    }
}

def make_table(table_name: str, table_data: list[dict[str, Any]]):
    """테이블을 생성하고 데이터를 삽입합니다."""
    schema = TABLE_SCHEMA.get(table_name)
    if not schema:
        print(f"Warning: {table_name}에 대한 스키마가 정의되지 않았습니다.")
        return

    columns = schema['columns']
    types = schema['types']

    # CREATE TABLE 문 생성
    create_columns = ', '.join([f'{col} {type_}' for col, type_ in zip(columns, types)])
    create_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({create_columns})'
    cursor.execute(create_sql)

    # INSERT 문 생성 및 데이터 삽입
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'

    for row_data in table_data:
        # 스키마에 정의된 컬럼 순서에 맞게 값 추출
        values = tuple(row_data.get(col) for col in columns)
        cursor.execute(insert_sql, values)

# 기존 데이터 가져오기
for json_file in DATA_FILES:
    json_path = os.path.join(DATA_PATH, json_file)
    table_name = json_file.split(".")[0]

    with open(json_path, 'r', encoding='utf-8') as json_data:
        data = json.load(json_data)
        make_table(table_name, data)

conn.commit()
conn.close()
print("데이터베이스 생성 완료!")
