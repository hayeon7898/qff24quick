from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
import time
import threading
from database.add_score import add_score
from database.parser import parse_question


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

# FastAPI 경로
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

def fetch_data_periodically():
    while True:
        try:
            response = requests.get("http://localhost:7000/get?")
            print("data:", response.json())
        except Exception as e:
            print("failed getting data:", e)
        
        time.sleep(10)  # 10초마다 요청

# 별도의 스레드에서 주기적으로 데이터 요청
threading.Thread(target=fetch_data_periodically, daemon=True).start()

@app.route('/receive', methods=['GET'])
def work():
    return jsonify({"status": "success", "message": "getting datas."})


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
