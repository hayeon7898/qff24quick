import sqlite3
from datetime import datetime

def add_score(username: str, type_id: str, problem_number: int, is_correct: bool):
    """유저의 점수를 저장하고 업데이트하는 함수."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # username으로 user_id 조회
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_result = cursor.fetchone()
        if not user_result:
            raise ValueError(f"User with username '{username}' does not exist.")
        user_id = user_result[0]

        # labs 테이블에서 type_id의 유효성 확인
        cursor.execute("SELECT id FROM labs WHERE lab_type = ?", (type_id,))
        lab_result = cursor.fetchone()
        if not lab_result:
            raise ValueError(f"Invalid lab_type: {type_id}")

        lab_id = lab_result[0]

        # sub_problems 테이블에서 문제 ID 조회
        cursor.execute(
            """
            SELECT id, max_score FROM sub_problems 
            WHERE lab_id = ? AND problem_number = ?
            """,
            (lab_id, problem_number)
        )
        sub_problem = cursor.fetchone()
        if not sub_problem:
            raise ValueError(f"No matching sub_problem for type {type_id} and problem {problem_number}")

        sub_problem_id, max_score = sub_problem

        # 기존 점수와 정답 여부 조회
        cursor.execute(
            """
            SELECT score, is_correct FROM scores 
            WHERE user_id = ? AND sub_problem_id = ?
            """,
            (user_id, sub_problem_id)
        )
        existing_score = cursor.fetchone()

        if existing_score:
            current_score, current_is_correct = existing_score

            # 기존 정답 여부와 같으면 업데이트 하지 않음
            if current_is_correct == is_correct:
                print("No change in correctness. Score update skipped.")
                return

            # 정답 여부가 변동된 경우 새로운 점수 계산
            new_score = max_score if is_correct else 0

            # 점수와 업데이트 시각 변경
            cursor.execute(
                """
                UPDATE scores
                SET score = ?, is_correct = ?, updated_at = ?
                WHERE user_id = ? AND sub_problem_id = ?
                """,
                (new_score, is_correct, datetime.now().isoformat(), user_id, sub_problem_id)
            )

            # 총점 조정 
            cursor.execute(
                """
                UPDATE users 
                SET total_score = total_score + ?, final_updated_at = ?
                WHERE id = ?
                """,
                (new_score, datetime.now().isoformat(), user_id)
            )
            print(f"Score updated: User {username} (ID: {user_id}), New Score {new_score}")

        else:
            # 신규 점수 삽입
            new_score = max_score if is_correct else 0
            cursor.execute(
                """
                INSERT INTO scores (user_id, sub_problem_id, score, is_correct, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, sub_problem_id, new_score, is_correct, datetime.now().isoformat())
            )

            # 총점 추가
            cursor.execute(
                """
                UPDATE users 
                SET total_score = total_score + ?
                WHERE id = ?
                """,
                (new_score, user_id)
            )
            print(f"Score added: User {username} (ID: {user_id}), Score {new_score}")

        # 해당 유저가 모든 하위 문제를 풀었는지 확인
        cursor.execute(
            """
            SELECT COUNT(*) FROM sub_problems WHERE lab_id = ? 
            """,
            (lab_id,)
        )
        total_problems = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*) FROM scores
            WHERE user_id = ? AND sub_problem_id IN (
                SELECT id FROM sub_problems WHERE lab_id = ?
            ) AND is_correct = 1
            """,
            (user_id, lab_id)
        )
        solved_problems = cursor.fetchone()[0]

        # Lab4에서 추가 점수 로직 수정 (Lab4만 다르게 처리)
        if type_id == 'lab4':
            group1 = [13, 14, 15, 16]
            group2 = [17, 18, 19, 20]

            cursor.execute(
                """
                SELECT COUNT(*) FROM scores
                WHERE user_id = ? AND sub_problem_id IN (
                    SELECT id FROM sub_problems WHERE lab_id = ? AND problem_number IN (?,?,?,?)
                ) AND is_correct = 1
                """,
                (user_id, lab_id, *group1)
            )
            group1_solved = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*) FROM scores
                WHERE user_id = ? AND sub_problem_id IN (
                    SELECT id FROM sub_problems WHERE lab_id = ? AND problem_number IN (?,?,?,?)
                ) AND is_correct = 1
                """,
                (user_id, lab_id, *group2)
            )
            group2_solved = cursor.fetchone()[0]

            if group1_solved == 4:
                print("Lab4 Group 1 (13-16) solved! Adding bonus score of 20.")
                cursor.execute(
                    """
                    UPDATE users 
                    SET total_score = total_score + 20
                    WHERE id = ?
                    """,
                    (user_id,)
                )
            if group2_solved == 4:
                print("Lab4 Group 2 (17-20) solved! Adding bonus score of 20.")
                cursor.execute(
                    """
                    UPDATE users 
                    SET total_score = total_score + 20
                    WHERE id = ?
                    """,
                    (user_id,)
                )

        elif solved_problems == total_problems:
            print("All sub-problems solved! Adding bonus score of 20.")
            cursor.execute(
                """
                UPDATE users 
                SET total_score = total_score + 20
                WHERE id = ?
                """,
                (user_id,)
            )

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as ve:
        print(f"Error: {ve}")
    finally:
        conn.close()
