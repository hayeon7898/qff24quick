from sqlalchemy.orm import Session
from app.models import Lab, SubProblem  # Assuming your models are in models.py

def parse_question(question: str, db: Session) -> tuple:
    # 숫자와 문자를 분리
    lab = int(question[0])  # 첫 번째 문자가 lab 번호
    type_id = f'lab{lab}'

    part = question[1]  # 두 번째 문자가 문제 세부 번호 (a, b, c, d 등)

    # 문제 번호 범위 설정 (이제 DB에서 가져올 예정)
    lab_record = db.query(Lab).filter(Lab.lab_type == type_id).first()
    if not lab_record:
        raise ValueError(f"Lab {lab} does not exist in the database.")

    # 세부 번호에 따라 문제 번호 결정
    # 'a'의 ASCII 코드가 97이므로 이를 기준으로 인덱스 계산
    base_number = lab_record.base_number
    problem_number = base_number + (ord(part) - ord('a'))
    
    # 결과 출력
    return type_id, problem_number

# 사용 예시:
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///your_database.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()

# print(parse_question("3e", db))  # 예시 출력: ('lab3', 28)
