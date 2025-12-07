import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DATABASE_URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL이 설정되지 않았습니다!")

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=False,  # SQL 쿼리 출력 (개발 중만, 운영 시 False)
    pool_pre_ping=True,  # 연결 확인 (끊긴 연결 재연결)
    pool_size=10,  # 연결 풀 크기
    max_overflow=20  # 추가 연결 최대 개수
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 모든 모델이 상속할 Base 클래스
Base = declarative_base()
