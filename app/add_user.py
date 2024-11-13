from app import db
from app.models import User
from datetime import datetime

# 사용자 추가 함수
def add_users():
    # 현재 시간을 설정
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 사용자 리스트
    users = [
        User(username="quick123", final_updated_at=current_time),
        User(username="quick456", final_updated_at=current_time),
        User(username="quick789", final_updated_at=current_time)
    ]

    # 세션에 추가
    db.session.add_all(users)
    
    # 변경 사항 커밋
    db.session.commit()