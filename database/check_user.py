import sqlite3

def check_user_in_db(user_id: str) -> bool:
    """user_id가 database에 존재하는지 확인."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (user_id,))
        user_exists = cursor.fetchone() is not None  # 존재 여부 확인
        return user_exists

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        conn.close()