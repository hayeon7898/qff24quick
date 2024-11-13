from app.models import Lab, SubProblem  # Assuming your models are in models.py

def parse_question(question: str) -> tuple:
    # 숫자와 문자를 분리
    lab = int(question[0])  # 첫 번째 문자가 lab 번호
    type_id = f'lab{lab}'

    # 1에서 6까지의 범위 확인
    if lab < 1 or lab > 6:
        return None  # lab이 범위를 벗어나면 None 반환

    # 각 lab 번호에 따른 기본 문제 번호
    if(lab==1): base_num=1
    elif(lab==2): base_num=5
    elif(lab==3): base_num=9
    elif(lab==4): base_num=15
    elif(lab==5): base_num=23
    else: base_num=27

    # 세부 문제 문자 (a, b, c, d 등)
    part = question[1]

    # 문제 번호 계산 (a의 ASCII 코드 97 기준)
    problem_number = base_num + (ord(part) - ord('a'))

    # 결과 반환
    return type_id, problem_number

# 사용 예시:
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///your_database.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()

#print(parse_question("3e"))  # 예시 출력: ('lab3', 28)
