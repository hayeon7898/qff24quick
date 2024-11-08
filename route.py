# from flask import Flask
from flask import render_template, jsonify, Flask
import sqlite3

app = Flask(__name__)

# 데이터베이스에서 데이터를 가져오는 함수
def get_user_scores():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 쿼리 작성: 유저별 점수와 순위를 가져오는 SQL 쿼리
    # 반복적인 부분을 사용하지 않도록 동적으로 쿼리 생성
    score_columns = ", ".join([
        f"SUM(CASE WHEN s.sub_problem_id = {i} THEN s.score ELSE 0 END) AS score{i}"
        for i in range(1, 29)
    ])
    
    query = f"""
        SELECT u.username, u.total_score,
               {score_columns},
               RANK() OVER (ORDER BY u.total_score DESC, MIN(u.final_updated_at) ASC) AS rank
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        GROUP BY u.id
        ORDER BY rank
    """
    
    cursor.execute(query)
    user_scores = cursor.fetchall()
    conn.close()
    return user_scores

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# 점수 데이터 API
@app.route('/scores')
def scores():
    user_scores = get_user_scores()
    return jsonify(user_scores)


# Flask 앱 실행
if __name__ == '__main__':
    app.run()
