from datetime import datetime
from app import app,db

# 테이블 정의
class Lab(db.Model):
    __tablename__ = 'labs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_type = db.Column(db.String, unique=True, nullable=False)

class SubProblem(db.Model):
    __tablename__ = 'sub_problems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    problem_number = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, default=10)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    total_score = db.Column(db.Integer, default=0)
    final_updated_at = db.Column(db.String, nullable=False)

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sub_problem_id = db.Column(db.Integer, db.ForeignKey('sub_problems.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    is_correct = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.String, nullable=False)


# 초기화 함수
def init_db():
    with app.app_context():
        if Lab.query.first() is not None:
            print("Database is already initialized.")
            return  # 이미 초기화된 경우 함수 종료

        db.create_all()  # 모든 테이블 생성

        # 초기 데이터 추가
        lab_types = ['lab1', 'lab2', 'lab3', 'lab4', 'lab5', 'lab6']
        for lab_type in lab_types:
            lab = Lab(lab_type=lab_type)
            db.session.add(lab)
        db.session.commit()

        # 각 랩에 대한 서브 문제 추가
        sub_problem_counts = [4, 4, 6, 8, 4, 5]
        labs = Lab.query.all()  # 모든 랩 데이터 가져오기

        problem_number = 1  # 문제 번호 초기화
        for index, lab in enumerate(labs):
            for _ in range(sub_problem_counts[index]):
                sub_problem = SubProblem(lab_id=lab.id, problem_number=problem_number)
                db.session.add(sub_problem)
                
                # scores 테이블에 초기 점수 추가
                current_time = datetime.now().isoformat()  # ISO 8601 형식으로 현재 시간 가져오기
                score_entry = Score(user_id=None, sub_problem_id=sub_problem.id, score=0, is_correct=False, updated_at=current_time)
                db.session.add(score_entry)

                problem_number += 1  # 문제 번호 증가
        db.session.commit()  # 모든 초기 데이터 저장
        print("Database initialized successfully.")
