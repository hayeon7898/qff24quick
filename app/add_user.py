from app import db
from app.models import User
from datetime import datetime
import random
import string

def generate_unique_usernames(count=40, length=6):
    usernames = set()
    while len(usernames) < count:
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        usernames.add(username)
    return list(usernames)

def add_users():
    # 유저 리스트 생성
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usernames = generate_unique_usernames()

    # 중복 여부 검수
    if len(usernames) == len(set(usernames)):
        print("중복 없음: 모든 사용자 이름이 고유합니다.")
    else:
        print("중복 있음: 사용자 이름에 중복이 있습니다.")

    # User 객체 생성
    users = [User(username=name, final_updated_at=current_time) for name in usernames]
    db.session.add_all(users)
    db.session.commit()

    # 생성된 사용자 리스트 출력
    for user in users:
        print(f"User(username='{user.username}', final_updated_at={user.final_updated_at})")


# # 사용자 추가 함수
# def add_users():
#     # 현재 시간을 설정
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # # 사용자 리스트
#     # users = [
#     #     User(username="quick123", final_updated_at=current_time),
#     #     User(username="quick456", final_updated_at=current_time),
#     #     User(username="quick789", final_updated_at=current_time)
#     # ]


#     # 세션에 추가
#     db.session.add_all(users)
    
#     # 변경 사항 커밋
#     db.session.commit()