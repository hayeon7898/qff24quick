from datetime import datetime
from app import db
from app.models import User, Score, Lab, SubProblem

def add_score(username: str, type_id: str, problem_number: int, is_correct: bool):
    """유저의 점수를 저장하고 업데이트하는 함수."""
    try:
        # username으로 user_id 조회
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError(f"User with username '{username}' does not exist.")

        # labs 테이블에서 type_id의 유효성 확인
        lab = Lab.query.filter_by(lab_type=type_id).first()
        if not lab:
            raise ValueError(f"Invalid lab_type: {type_id}")

        # sub_problems 테이블에서 문제 ID 조회
        sub_problem = SubProblem.query.filter_by(lab_id=lab.id, problem_number=problem_number).first()
        if not sub_problem:
            raise ValueError(f"No matching sub_problem for type {type_id} and problem {problem_number}")

        # 기존 점수와 정답 여부 조회
        existing_score = Score.query.filter_by(user_id=user.id, sub_problem_id=sub_problem.id).first()

        if existing_score:
            # 기존 정답 여부와 같으면 업데이트 하지 않음
            if existing_score.is_correct == is_correct:
                print("No change in correctness. Score update skipped.")
                return

            # 정답 여부가 변동된 경우 새로운 점수 계산
            new_score = sub_problem.max_score if is_correct else 0

            # 점수와 업데이트 시각 변경
            existing_score.score = new_score
            existing_score.is_correct = is_correct
            existing_score.updated_at = datetime.now()

            # 총점 조정 
            user.total_score += new_score
            user.final_updated_at = datetime.now()
            print(f"Score updated: User {username} (ID: {user.id}), New Score {new_score}")

        else:
            # 신규 점수 삽입
            new_score = sub_problem.max_score if is_correct else 0
            new_score_entry = Score(
                user_id=user.id,
                sub_problem_id=sub_problem.id,
                score=new_score,
                is_correct=is_correct,
                updated_at=datetime.now()
            )
            db.session.add(new_score_entry)

            # 총점 추가
            user.total_score += new_score
            print(f"Score added: User {username} (ID: {user.id}), Score {new_score}")

        # 해당 유저가 모든 하위 문제를 풀었는지 확인
        total_problems = SubProblem.query.filter_by(lab_id=lab.id).count()

        solved_problems = Score.query.filter(
            Score.user_id == user.id,
            Score.sub_problem_id.in_(db.session.query(SubProblem.id).filter_by(lab_id=lab.id)),
            Score.is_correct == 1
        ).count()

        # Lab4에서 추가 점수 로직 수정 (Lab4만 다르게 처리)
        if type_id == 'lab4':
            group1 = [13, 14, 15, 16]
            group2 = [17, 18, 19, 20]

            group1_solved = Score.query.filter(
                Score.user_id == user.id,
                Score.sub_problem_id.in_(db.session.query(SubProblem.id).filter_by(lab_id=lab.id, problem_number=group1)),
                Score.is_correct == 1
            ).count()

            group2_solved = Score.query.filter(
                Score.user_id == user.id,
                Score.sub_problem_id.in_(db.session.query(SubProblem.id).filter_by(lab_id=lab.id, problem_number=group2)),
                Score.is_correct == 1
            ).count()

            if group1_solved == 4:
                print("Lab4 Group 1 (13-16) solved! Adding bonus score of 20.")
                user.total_score += 20
            if group2_solved == 4:
                print("Lab4 Group 2 (17-20) solved! Adding bonus score of 20.")
                user.total_score += 20

        elif solved_problems == total_problems:
            print("All sub-problems solved! Adding bonus score of 20.")
            user.total_score += 20

        # Commit the changes to the database
        db.session.add(user)
        db.session.commit()

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Database error: {e}")
        db.session.rollback()
    finally:
        # No need to manually close the connection with SQLAlchemy; it's handled by the session.
        pass
