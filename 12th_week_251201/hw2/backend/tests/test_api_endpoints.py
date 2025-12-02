"""
SNS API 엔드포인트 테스트 케이스
"""
import pytest


class TestGetUsersEndpoint:
    """GET /api/all_users 테스트"""

    def test_get_users_success(self, client):
        """사용자 목록 조회 성공"""
        response = client.get("/api/all_users")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "success"
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_users_data_structure(self, client):
        """사용자 데이터 구조 검증"""
        response = client.get("/api/all_users")
        assert response.status_code == 200
        data = response.json()

        if len(data["data"]) > 0:
            user = data["data"][0]
            assert "id" in user
            assert "email" in user
            assert "nickname" in user
            # profile_image는 optional

    def test_get_users_not_empty(self, client):
        """사용자 데이터가 존재"""
        response = client.get("/api/all_users")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0, "사용자 데이터가 비어있습니다"


class TestGetPostsEndpoint:
    """GET /api/all_posts 테스트"""

    def test_get_posts_success(self, client):
        """게시글 목록 조회 성공"""
        response = client.get("/api/all_posts")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "success"
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_posts_data_structure(self, client):
        """게시글 데이터 구조 검증"""
        response = client.get("/api/all_posts")
        assert response.status_code == 200
        data = response.json()

        if len(data["data"]) > 0:
            post = data["data"][0]
            assert "id" in post
            assert "title" in post
            assert "author" in post
            assert "contents" in post
            assert "like_count" in post
            assert "reply_count" in post
            assert "view_count" in post
            assert "last_upload_at" in post

    def test_get_posts_not_empty(self, client):
        """게시글 데이터가 존재"""
        response = client.get("/api/all_posts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0, "게시글 데이터가 비어있습니다"

    def test_get_posts_counts_are_integers(self, client):
        """게시글 카운트 필드가 정수"""
        response = client.get("/api/all_posts")
        assert response.status_code == 200
        data = response.json()

        for post in data["data"]:
            assert isinstance(post["like_count"], int), "like_count는 정수여야 합니다"
            assert isinstance(post["reply_count"], int), "reply_count는 정수여야 합니다"
            assert isinstance(post["view_count"], int), "view_count는 정수여야 합니다"


class TestGetPostDetailEndpoint:
    """GET /api/post 테스트"""

    def test_get_post_detail_success(self, client):
        """게시글 상세 조회 성공"""
        # 먼저 게시글 목록에서 ID 가져오기
        list_response = client.get("/api/all_posts")
        posts = list_response.json()["data"]

        if len(posts) > 0:
            post_id = posts[0]["id"]
            response = client.get(f"/api/post?post_id={post_id}")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["message"] == "success"
            assert "data" in data

    def test_get_post_detail_data_structure(self, client):
        """게시글 상세 데이터 구조 검증"""
        # 먼저 게시글 목록에서 ID 가져오기
        list_response = client.get("/api/all_posts")
        posts = list_response.json()["data"]

        if len(posts) > 0:
            post_id = posts[0]["id"]
            response = client.get(f"/api/post?post_id={post_id}")
            assert response.status_code == 200
            data = response.json()
            detail_post = data["data"][0]

            assert "id" in detail_post
            assert "title" in detail_post
            assert "author" in detail_post
            assert "contents" in detail_post

    def test_get_post_detail_empty_post_id(self, client):
        """post_id가 빈 값일 때"""
        response = client.get("/api/post?post_id=")
        assert response.status_code == 400

    def test_get_post_detail_invalid_post_id(self, client):
        """존재하지 않는 post_id"""
        response = client.get("/api/post?post_id=nonexistent_id_12345")
        # 204 (No Content) 또는 404 반환 가능
        assert response.status_code in [204, 404]

    def test_get_post_detail_required_parameter(self, client):
        """post_id 파라미터 없음"""
        response = client.get("/api/post")
        # 422 (Unprocessable Entity) 반환
        assert response.status_code == 422


class TestGetRepliesEndpoint:
    """GET /api/all_replies 테스트"""

    def test_get_replies_success(self, client):
        """댓글 목록 조회 성공"""
        response = client.get("/api/all_replies")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "success"
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_replies_data_structure(self, client):
        """댓글 데이터 구조 검증"""
        response = client.get("/api/all_replies")
        assert response.status_code == 200
        data = response.json()

        if len(data["data"]) > 0:
            reply = data["data"][0]
            assert "post_id" in reply
            assert "author" in reply
            assert "contents" in reply
            assert "last_upload_at" in reply

    def test_get_replies_not_empty(self, client):
        """댓글 데이터가 존재"""
        response = client.get("/api/all_replies")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0, "댓글 데이터가 비어있습니다"


class TestDataConsistency:
    """데이터 일관성 테스트"""

    def test_reply_count_accuracy(self, client):
        """게시글의 reply_count가 실제 댓글 수와 일치"""
        # 게시글 목록 조회
        posts_response = client.get("/api/all_posts")
        posts = posts_response.json()["data"]

        # 댓글 목록 조회
        replies_response = client.get("/api/all_replies")
        all_replies = replies_response.json()["data"]

        # 각 게시글의 reply_count 검증
        for post in posts:
            actual_reply_count = sum(1 for reply in all_replies if reply["post_id"] == post["id"])
            assert post["reply_count"] == actual_reply_count, \
                f"Post {post['id']}: reply_count={post['reply_count']}, actual={actual_reply_count}"

    def test_posts_and_replies_have_matching_ids(self, client):
        """게시글과 댓글의 관계 검증"""
        posts_response = client.get("/api/all_posts")
        posts = posts_response.json()["data"]
        post_ids = {post["id"] for post in posts}

        replies_response = client.get("/api/all_replies")
        all_replies = replies_response.json()["data"]

        # 모든 댓글의 post_id가 존재하는 게시글 ID여야 함
        for reply in all_replies:
            assert reply["post_id"] in post_ids, \
                f"Reply {reply.get('id')} has invalid post_id: {reply['post_id']}"

    def test_authors_exist_in_users(self, client):
        """게시글과 댓글의 author가 존재하는 사용자여야 함 (선택사항)"""
        users_response = client.get("/api/all_users")
        users = users_response.json()["data"]
        user_nicknames = {user["nickname"] for user in users}

        posts_response = client.get("/api/all_posts")
        posts = posts_response.json()["data"]

        # 모든 게시글의 author가 존재하는 사용자여야 함
        for post in posts:
            assert post["author"] in user_nicknames, \
                f"Post author '{post['author']}' not found in users"


class TestResponseFormats:
    """응답 형식 테스트"""

    def test_all_endpoints_return_json(self, client):
        """모든 엔드포인트가 JSON 형식 반환"""
        endpoints = ["/api/all_users", "/api/all_posts", "/api/all_replies"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.headers["content-type"] == "application/json"

    def test_status_codes_correct(self, client):
        """올바른 HTTP 상태 코드 반환"""
        # 200 OK
        assert client.get("/api/all_users").status_code == 200
        assert client.get("/api/all_posts").status_code == 200
        assert client.get("/api/all_replies").status_code == 200

        # 400 Bad Request
        assert client.get("/api/post?post_id=").status_code == 400

        # 422 Unprocessable Entity (missing required parameter)
        assert client.get("/api/post").status_code == 422
