"""
샘플 데이터 생성 스크립트
데이터베이스에 테스트용 데이터 10개씩 생성
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# 환경 변수 로드
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ORM 모델 임포트
from backend.db.config import Base
from backend.db.models import UserDB, PostDB, RelayStoryDB

# 비밀번호 해싱 (bcrypt는 최대 72바이트까지만 지원)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 기본 라운드 수 설정
)

# 데이터베이스 연결
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def seed_users(db, num: int = 10):
    """샘플 사용자 데이터 생성"""
    print(f"\n{'='*50}")
    print(f"👥 {num}명의 샘플 사용자 생성 중...")
    print(f"{'='*50}")
    
    users_data = [
        {
            "nickname": "alice_wonder",
            "email": "alice@example.com",
            "password": "",
            "profile_photo": "https://i.pravatar.cc/150?img=1"
        }
    ]
    
    users = []
    for data in users_data[:num]:
        user = UserDB(
            nickname=data["nickname"],
            email=data["email"],
            password_hash=hash_password(data["password"]),
            profile_photo=data["profile_photo"],
            created_at=datetime.utcnow() - timedelta(days=30)
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    for user in users:
        db.refresh(user)
    
    print(f"✅ {len(users)}명의 사용자가 생성되었습니다!")
    for user in users:
        print(f"   - {user.nickname} ({user.email})")
    
    return users

def seed_posts(db, users, num: int = 10):
    """샘플 게시물 데이터 생성"""
    print(f"\n{'='*50}")
    print(f"📝 {num}개의 샘플 게시물 생성 중...")
    print(f"{'='*50}")
    
    posts_data = [
        {
            "title": "AI가 미래의 창작을 어떻게 바꿀까?",
            "content": "인공지능은 문학, 미술, 음악 등 창작 활동을 근본적으로 변화시키고 있습니다. 이 글에서는 AI가 창작에 미치는 긍정적, 부정적 영향을 살펴봅니다.",
            "genre": "인공지능",
            "next_story_count": 8
        },
        {
            "title": "기후변화와의 싸움: 우리의 선택",
            "content": "지구 온난화는 더 이상 먼 미래의 문제가 아닙니다. 개인과 사회가 함께 노력할 수 있는 방법들을 모아봤습니다.",
            "genre": "환경",
            "next_story_count": 6
        },
        {
            "title": "대우주 시대의 우주 탐사",
            "content": "NASA, SpaceX, 그리고 다른 우주 기관들이 화성으로의 미션을 준비하고 있습니다. 우주 탐사의 미래는?",
            "genre": "우주",
            "next_story_count": 10
        },
        {
            "title": "의료 기술의 혁명: 원격진료",
            "content": "팬데믹 이후 원격진료가 급속도로 확산되고 있습니다. 이 기술이 의료 체계를 어떻게 변화시킬까요?",
            "genre": "의학",
            "next_story_count": 7
        },
        {
            "title": "게임 산업의 미래",
            "content": "메타버스, VR, 클라우드 게이밍... 게임 산업은 빠르게 진화하고 있습니다. 다음 세대 게임은 어떤 모습일까?",
            "genre": "게임",
            "next_story_count": 9
        },
        {
            "title": "지속 가능한 패션의 시대",
            "content": "빠스트 패션의 문제점을 인식한 소비자들이 지속 가능한 의류를 찾고 있습니다. 이 트렌드가 산업을 어떻게 바꿀까?",
            "genre": "패션",
            "next_story_count": 5
        },
        {
            "title": "블록체인이 정말 미래를 바꿀까?",
            "content": "암호화폐부터 스마트 계약까지, 블록체인 기술의 가능성과 한계를 살펴봅니다.",
            "genre": "금융",
            "next_story_count": 8
        },
        {
            "title": "뇌-컴퓨터 인터페이스: 꿈인가 현실인가?",
            "content": "Neuralink 같은 회사들이 뇌와 컴퓨터를 직접 연결하려는 시도를 하고 있습니다. 이것이 가능할까?",
            "genre": "미래",
            "next_story_count": 12
        },
        {
            "title": "원격 근무의 장단점",
            "content": "팬데믹 이후 원격 근무가 새로운 표준이 되었습니다. 장점과 단점을 균형있게 살펴봅시다.",
            "genre": "일",
            "next_story_count": 6
        },
        {
            "title": "양자 컴퓨팅의 혁명이 오는가?",
            "content": "양자 컴퓨팅이 현실화되면 기존의 암호화 방식이 무용지물이 될 수 있습니다. 미래를 준비해야 할까?",
            "genre": "양자 컴퓨팅",
            "next_story_count": 10
        }
    ]
    
    posts = []
    for i, data in enumerate(posts_data[:num]):
        # 라운드 로빈으로 다양한 사용자가 게시물 작성하도록
        user = users[i % len(users)]
        
        post = PostDB(
            title=data["title"],
            content=data["content"],
            genre=data["genre"],
            author=user.nickname,
            user_id=user.id,
            next_story_count=data["next_story_count"],
            created_at=datetime.utcnow() - timedelta(days=20 - i)
        )
        db.add(post)
        posts.append(post)
    
    db.commit()
    for post in posts:
        db.refresh(post)
    
    print(f"✅ {len(posts)}개의 게시물이 생성되었습니다!")
    for post in posts:
        print(f"   - [{post.id}] {post.title} (작성자: {post.author}, 목표: {post.next_story_count}명)")
    
    return posts

def seed_relay_stories(db, posts, users, num_per_post: int = 3):
    """샘플 릴레이 스토리 데이터 생성"""
    print(f"\n{'='*50}")
    print(f"💬 샘플 릴레이 스토리 생성 중...")
    print(f"{'='*50}")
    
    relay_stories_data = [
        # Post 1 (8개 목표)
        [
            "AI는 이미 우리 생활의 많은 부분에 침투해 있습니다. 음악 추천부터 사진 편집까지 말이에요.",
            "맞아요. 하지만 정말 창조적인 작품을 만들 수 있을까요? AI가 만든 음악이나 미술작품이 감정을 전달할 수 있을까?",
            "흥미로운 질문입니다. 어쩌면 인간과 AI의 협력이 가장 좋은 결과를 만들 수도 있어요."
        ],
        # Post 2 (6개 목표)
        [
            "개인적으로는 재활용을 더 철저히 해야 한다고 생각합니다.",
            "맞아요. 하지만 개인의 노력만으로는 부족합니다. 정부와 기업의 정책 변화가 필요해요.",
            "정확해요. 탄소세 같은 정책들이 실질적인 변화를 만들 수 있죠."
        ],
        # Post 3 (10개 목표)
        [
            "화성 미션은 정말 인류 역사상 위대한 도전이 될 거 같습니다!",
            "동의합니다! 하지만 기술적, 재정적 문제들이 많이 남아있어요.",
            "그렇지만 우주 여행이 더 대중화되면 어떨까요? 미래의 우주 관광?"
        ],
        # Post 4 (7개 목표)
        [
            "원격진료는 시골 지역 의료 접근성을 크게 높였어요.",
            "맞습니다. 하지만 개인정보 보안이 정말 중요해집니다.",
            "네, 의료 데이터 암호화 기술도 함께 발전해야 해요."
        ],
        # Post 5 (9개 목표)
        [
            "메타버스에서 친구들과 만나는 경험은 정말 신기해요.",
            "VR 기술이 더 발전하면 진짜 만나는 것 같은 느낌을 줄 수 있을 거 같아요.",
            "네, 그때쯤이면 게임과 현실의 경계가 희미해질 거 같습니다."
        ],
        # Post 6 (5개 목표)
        [
            "지속 가능한 의류는 비싸지만 환경을 생각하면 가치가 있어요.",
            "맞아요. 기업들도 점차 환경 친화적 소재를 개발하고 있어요.",
            "미래에는 모든 의류가 지속 가능해져야 합니다."
        ],
        # Post 7 (8개 목표)
        [
            "블록체인은 금융뿐만 아니라 모든 산업을 바꿀 잠재력이 있어요.",
            "동의하지만, 아직 확장성 문제가 남아있습니다.",
            "네, 하지만 기술이 빠르게 발전하고 있으니까요."
        ],
        # Post 8 (12개 목표)
        [
            "뇌-컴퓨터 인터페이스가 현실화되면 장애인들의 삶이 크게 나아질 거 같아요.",
            "정확합니다. 거동불능인 사람들이 다시 활동할 수 있게 되겠네요.",
            "하지만 윤리적 문제들도 많아요. 뇌 해킹 같은 거 말이에요."
        ],
        # Post 9 (6개 목표)
        [
            "원격 근무는 유연성이 좋지만, 회사 문화를 약화시킬 수 있어요.",
            "맞아요. 온라인 협업 도구들이 발전했지만 대면의 가치는 여전해요.",
            "하이브리드 방식이 최선의 방법일 수도 있겠네요."
        ],
        # Post 10 (10개 목표)
        [
            "양자 컴퓨팅이 상용화되면 현재의 인터넷 보안 체계가 무너질 거 같아요.",
            "그렇기 때문에 양자 암호화(Post-Quantum Cryptography)가 중요해요.",
            "미래에는 모든 시스템이 양자-안전 기술로 업그레이드될 거 같습니다."
        ]
    ]
    
    relay_stories = []
    story_index = 0
    
    for post in posts[:num_per_post]:
        # 각 게시물에 3-4개의 릴레이 스토리 추가
        num_stories = min(3, post.next_story_count)
        
        for j in range(num_stories):
            if story_index < len(relay_stories_data[posts.index(post)]):
                user = users[(j + posts.index(post)) % len(users)]
                
                relay_story = RelayStoryDB(
                    content=relay_stories_data[posts.index(post)][j],
                    author=user.nickname,
                    user_id=user.id,
                    post_id=post.id,
                    created_at=post.created_at + timedelta(hours=j+1)
                )
                db.add(relay_story)
                relay_stories.append(relay_story)
    
    db.commit()
    for story in relay_stories:
        db.refresh(story)
    
    print(f"✅ {len(relay_stories)}개의 릴레이 스토리가 생성되었습니다!")
    for story in relay_stories:
        print(f"   - [{story.id}] Post #{story.post_id}: {story.author} - '{story.content[:50]}...'")
    
    return relay_stories

def main():
    """메인 함수: 모든 샘플 데이터 생성"""
    print("\n" + "="*50)
    print("🌱 샘플 데이터 생성을 시작합니다...")
    print("="*50)
    
    # 데이터베이스 초기화 (테이블 생성)
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료!")
    
    db = SessionLocal()
    
    try:
        # 기존 데이터 확인
        existing_users = db.query(UserDB).count()
        if existing_users > 0:
            print(f"\n⚠️  이미 {existing_users}개의 데이터가 있습니다.")
            response = input("기존 데이터를 삭제하고 새로 생성하시겠습니까? (y/n): ")
            
            if response.lower() == 'y':
                print("\n🗑️  기존 데이터 삭제 중...")
                db.query(RelayStoryDB).delete()
                db.query(PostDB).delete()
                db.query(UserDB).delete()
                db.commit()
                print("✅ 기존 데이터가 삭제되었습니다!")
            else:
                print("취소되었습니다.")
                return
        
        # 샘플 데이터 생성
        users = seed_users(db, num=10)
        posts = seed_posts(db, users, num=10)
        relay_stories = seed_relay_stories(db, posts, users, num_per_post=3)
        
        # 최종 요약
        print(f"\n{'='*50}")
        print("📊 데이터 생성 완료!")
        print(f"{'='*50}")
        print(f"✅ 사용자: {len(users)}명")
        print(f"✅ 게시물: {len(posts)}개")
        print(f"✅ 릴레이 스토리: {len(relay_stories)}개")
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()