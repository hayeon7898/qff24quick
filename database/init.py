import sqlite3
from datetime import datetime

def init_db():
    # database.db 파일이 없다면 새로 생성하고 연결
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 테이블 생성 (위에서 작성한 것과 동일)
    cursor.execute(''' 
    CREATE TABLE labs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_type TEXT UNIQUE NOT NULL
    );  
    ''')
    
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS sub_problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_id INTEGER NOT NULL,
        problem_number INTEGER NOT NULL,
        max_score INTEGER DEFAULT 10,
        FOREIGN KEY (lab_id) REFERENCES labs(id)
    );
    ''')
    
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        total_score INTEGER DEFAULT 0,
        final_updated_at TEXT UNIQYE NOT NULL
    );
    ''')
    
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sub_problem_id INTEGER NOT NULL,
        score INTEGER DEFAULT 0,
        is_correct BOOLEAN DEFAULT 0,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (sub_problem_id) REFERENCES sub_problems(id)
    );
    ''')

    lab_types = ['lab1', 'lab2', 'lab3', 'lab4', 'lab5', 'lab6'] 
    for lab_type in lab_types:
        cursor.execute('INSERT OR IGNORE INTO labs (lab_type) VALUES (?);', (lab_type,))

    # 서브 문제 개수 설정: 각 랩에 해당하는 서브문제 수
    sub_problem_counts = [4, 4, 6, 8, 4, 5]

    # 서브 문제를 할당하기 위한 문제 번호 추적
    problem_number = 1
    
    cursor.execute('SELECT id FROM labs;')
    lab_ids = cursor.fetchall()

    # 각 랩에 대해 서브문제를 추가
    for lab_index, lab_id in enumerate(lab_ids):
        lab_id = lab_id[0]
        num_sub_problems = sub_problem_counts[lab_index]
        
        for _ in range(num_sub_problems):
            # sub_problems에 문제 추가
            cursor.execute('INSERT INTO sub_problems (lab_id, problem_number) VALUES (?, ?);', (lab_id, problem_number))
            
            # 방금 추가한 sub_problem의 ID를 가져옴
            sub_problem_id = cursor.lastrowid
            
            # 현재 시간 가져오기
            current_time = datetime.now().isoformat()  # ISO 8601 형식으로 현재 시간 가져오기
            
            # scores 테이블에 초기 점수 추가
            cursor.execute('INSERT INTO scores (user_id, sub_problem_id, score, is_correct, updated_at) VALUES (?, ?, ?, ?, ?);', 
                           (None, sub_problem_id, 0, 0, current_time))  # user_id는 None이지만, 필요에 따라 초기화 가능
            
            problem_number += 1  # 문제 번호 증가
    # ...
    # 테이블 목록 확인 (디버그)
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    # labs 테이블 내용 확인 (디버그)
    cursor.execute('SELECT * FROM labs;')
    labs = cursor.fetchall()
    print("Labs in database:", labs)

    # sub_problems 테이블 내용 확인 (디버그)
    cursor.execute('SELECT * FROM sub_problems;')
    sub_problems = cursor.fetchall()
    print("Sub Problems in database:", sub_problems)

    # scores 테이블 내용 확인 (디버그)
    cursor.execute('SELECT * FROM scores;')
    scores = cursor.fetchall()
    print("Scores in database:", scores)

    conn.commit()    
    conn.close()

# DB 초기화 실행
if __name__ == "__main__":
    init_db()
