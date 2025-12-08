<!-- 사용자 테이블 -->
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_photo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

<!-- 포스트 테이블 -->
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    next_story_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

<!-- 릴레이 이야기 테이블 -->
CREATE TABLE relay_stories (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    author VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

<!-- 인덱스 -->
-- users 테이블 인덱스
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_nickname ON users(nickname);

-- posts 테이블 인덱스
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_author ON posts(author);

-- relay_stories 테이블 인덱스
CREATE INDEX idx_relay_stories_post_id ON relay_stories(post_id);
CREATE INDEX idx_relay_stories_user_id ON relay_stories(user_id);
CREATE INDEX idx_relay_stories_created_at ON relay_stories(created_at DESC);
CREATE INDEX idx_relay_stories_author ON relay_stories(author);

-- 복합 인덱스 (자주 함께 조회되는 컬럼)
CREATE INDEX idx_relay_stories_post_created ON relay_stories(post_id, created_at DESC);