from fastapi import HTTPException
from fastapi.responses import Response
import datetime, time
from models.db_models import get_all_table_datas, where_post_id
from models.db_models import UserModel, PostModel, ReplyModel

# 사용자 목록 조회
def get_users():
    try:
        data = get_all_table_datas('user')
        user_list: list[UserModel] = [UserModel(**user) for user in data]
        return {"message": "success", "data": user_list}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="no_data")
    
# 게시글 목록 조회
def get_posts():
    try:
        data = get_all_table_datas('posts')
        post_list: list[PostModel] = [PostModel(**post) for post in data]
        return {"message": "success", "data": post_list}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="no_data")
    
# 게시글 상세 조회
def get_post_detail(post_id: str):
    if post_id == '':
        raise HTTPException(status_code=400, detail="no_value_in_query")
    
    try:
        data = where_post_id(post_id)
        if len(data) != 0:
            return {"message": "success", "data": data}
        else:
            return Response(status_code=204)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail="internal_error")

# 댓글 목록 조회
def get_replies():
    try:
        data = get_all_table_datas('reply')
        reply_list: list[ReplyModel] = [ReplyModel(**reply) for reply in data]
        return {"message": "success", "data": reply_list}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="no_data")
    