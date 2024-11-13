from app import db
from app.models import Lab, SubProblem

# lab1에 해당하는 SubProblem들의 문제 번호 출력
lab1 = Lab.query.filter_by(lab_type='lab1').first()  # lab1 가져오기
if lab1:
    sub_problems = SubProblem.query.filter_by(lab_id=lab1.id).all()  # lab1의 모든 SubProblem 가져오기
    for sub_problem in sub_problems:
        print(f"SubProblem ID: {sub_problem.id}, Problem Number: {sub_problem.problem_number}")
else:
    print("Lab1 not found")
