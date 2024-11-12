from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
import os
from database.init import init_db
from database import add_user 
from database.add_score import add_score
from database.parser import parse_question


db_path = 'database.db'

if not os.path.exists(db_path):
    init_db()
    add_user


# 데이터베이스에서 데이터를 가져오는 함수
def get_user_scores():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    score_columns = ", ".join([
        f"SUM(CASE WHEN s.sub_problem_id = {i} THEN s.score ELSE 0 END) AS score{i}"
        for i in range(1, 32)
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

app = Flask(__name__)
CORS(app)

# Flask 경로
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scores")
def scores():
    return jsonify(get_user_scores())

# 1번 시도
#@app.route('/endpoint', methods=['POST'])
#def receive_data():
#    data = request.json
#    username = data.get("username")
#    question = data.get("question")
#    grading_validation = data.get("grading_validation")
#    
#    type_id, problem_number = parse_question(question)
#   add_score(username, type_id, problem_number, grading_validation)
#
#    return jsonify({"message": f"Received data for {username}, {question} with validation: {grading_validation}"})

# 2번 시도
# def fetch_data_periodically():
#     while True:
#         try:
#             response = requests.get("http://127.0.0.0:8000/get", timeout=20)
#             print("data:", response.json())
#         except Exception as e:
#             print("failed getting data:", e)
    
#         time.sleep(10)  # 10초마다 요청
# threading.Thread(target=fetch_data_periodically, daemon=True).start()

# @app.route('/receive', methods=['GET'])
# def receive():
#     return jsonify({"status": "success", "message": "getting datas."})

@app.route('/receive-data', methods=['POST'])
def receive_data():
    try:
        # FastAPI 서버로부터 데이터를 받음
        data = request.get_json()

        # 필요한 정보 추출
        username = data['username']
        question = data['question']
        answer = data['answer']

        # 데이터를 처리하고 응답 생성 (예: 데이터베이스에 저장, 로그 출력 등)
        response = {
            "message": "Data received successfully",
            "received_data": {
                "username": username,
                "question": question,
                "answer": answer
            }
        }

        type_id, problem_number = parse_question(question)
        add_score(username, type_id, problem_number, answer)

        # 성공적으로 데이터를 받았다면 JSON으로 응답
        return jsonify(response), 200

    except Exception as e:
        # 오류가 발생하면 오류 메시지와 함께 응답
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
