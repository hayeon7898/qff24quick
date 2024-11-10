import sqlite3
from add_score import add_score

# 점수 추가를 위한 예제 실행
user_id = 'quick123'

# lab1의 1~4번 문제를 정답으로 추가
for problem_number in range(1, 5):
    add_score(user_id, 'lab1', problem_number, is_correct=True)

# lab2의 2번 문제를 정답으로 추가
add_score(user_id, 'lab2', 7, is_correct=True)

#lab4의 4~8번 문제 정답으로 추가
for problem_number in range(17, 21):
    add_score(user_id, 'lab4', problem_number, is_correct=True)

# 존재하지 않는 lab
try:
    add_score(user_id, 'lab7', 29, is_correct=True)
except ValueError as ve:
    print(f"Error while adding score for lab6, problem 1: {ve}")

# 해당 lab과 subproblem number 불일치
try:
    add_score(user_id, 'lab6', 3, is_correct=True)
except ValueError as ve:
    print(f"Error while adding score for lab3, problem 6: {ve}")

try:
    add_score(user_id, 'lab6', 29, is_correct=True)
except ValueError as ve:
    print(f"Error while adding score for lab3, problem 6: {ve}")

user_id = 'quick456'
for problem_number in range(13, 21):
    add_score(user_id, 'lab4', problem_number, is_correct=True)

user_id = 'quick789'
for problem_number in range(13, 21):
    add_score(user_id, 'lab4', problem_number, is_correct=True)
for problem_number in range(25, 29):
    add_score(user_id, 'lab6', problem_number, is_correct=True)

user_id = 'quick456'
for problem_number in range(25, 29):
    add_score(user_id, 'lab6', problem_number, is_correct=True)





# user의 총점 확인 함수
def get_user_score(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT total_score FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()

        if result:
            total_score = result[0]
            print(f"User {username} has a total score of {total_score}")
        else:
            print(f"User with ID {username} not found.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

get_user_score('quick123')

user_id = 'quick123'
add_score(user_id, 'lab5', 22, is_correct=True)
