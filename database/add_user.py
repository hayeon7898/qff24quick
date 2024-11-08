import sqlite3
from datetime import datetime

def add_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # 새로운 유저 추가
        cursor.execute('INSERT INTO users (username, total_score, final_updated_at) VALUES (?, ?, ?)', (username, 0, datetime.now().isoformat()))
        user_id = cursor.lastrowid  # 추가된 유저의 ID 가져오기

        # 모든 하위 문제에 대해 기본 점수(0점) 설정
        cursor.execute('SELECT id FROM sub_problems')
        sub_problem_ids = cursor.fetchall()

        for sub_problem_id in sub_problem_ids:
            cursor.execute('''INSERT INTO scores (user_id, sub_problem_id, score, is_correct, updated_at) 
                              VALUES (?, ?, ?, ?, datetime('now'))''', 
                           (user_id, sub_problem_id[0], 0, False))
        
        conn.commit()
        print(f"User '{username}' added successfully with default scores!")

    except sqlite3.IntegrityError:
        # username 중복 또는 무결성 제약 위반 시
        print(f"Error: User '{username}' already exists.")

    except sqlite3.Error as e:
        # 기타 DB 관련 에러 처리
        print(f"Database error: {e}")

    finally:
        conn.close()

# 예시 실행
if __name__ == "__main__":
    add_user('quick123')
    add_user('quick456')
    add_user('quick789')
