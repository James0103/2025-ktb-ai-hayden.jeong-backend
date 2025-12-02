from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional, Any
import os, json
import sqlite3

class UserModel(BaseModel):
    id: str
    email: str
    nickname: str
    profile_image: Optional[str] = None

class PostModel(BaseModel):
    id: str
    title: str
    author: str
    contents: Optional[str]
    like_count: int
    reply_count: int
    view_count: int
    last_upload_at: str
    img: Optional[str]

class ReplyModel(BaseModel):
    id: Optional[str]
    post_id: str
    author: str
    contents: str
    last_upload_at: str

def __get_db() -> sqlite3.Connection:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(script_dir, '..', 'db')
    conn = sqlite3.connect(os.path.join(DATA_PATH, 'sns.db'))
    return conn

def get_all_table_datas(table_name: str):
    conn = __get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    match table_name:
        case 'user':
            cursor.execute('SELECT * FROM user')
        case 'posts':
            cursor.execute('SELECT * FROM posts')
        case 'reply':
            cursor.execute('SELECT * FROM reply')

    all_data = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return all_data

def count_replies_by_post_id(post_id: str) -> int:
    """특정 post_id의 댓글 개수를 조회"""
    conn = __get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM reply WHERE post_id = ?', (post_id,))

    result = cursor.fetchone()
    count = result[0] if result else 0
    cursor.close()
    conn.close()

    return count

def where_post_id(post_id: str):
    conn = __get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))

    post_data = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return post_data