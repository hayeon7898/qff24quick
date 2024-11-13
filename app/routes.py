from flask import render_template, jsonify, request
import requests
from app.add_score import add_score
from app.parser import parse_question
from sqlalchemy import func,case,bindparam,text
from app import app,db
from app.models import User, Score, SubProblem 
from datetime import datetime
import json



# # 데이터베이스에서 데이터를 가져오는 함수
# def get_user_scores():
#     score_columns = ", ".join([
#         f"SUM(CASE WHEN s.sub_problem_id = {i} THEN s.score ELSE 0 END) AS score{i}"
#         for i in range(1, 32)
#     ])
    
#     query = f"""
#         SELECT u.username, u.total_score,
#                {score_columns},
#                RANK() OVER (ORDER BY u.total_score DESC, MIN(u.final_updated_at) ASC) AS rank
#         FROM users u
#         LEFT JOIN scores s ON u.id = s.user_id
#         GROUP BY u.id
#         ORDER BY rank
#     """
    
#     cursor.execute(query)
#     user_scores = cursor.fetchall()
#     conn.close()
#     return user_scores

# app = Flask(__name__)
# CORS(app)

def get_user_scores():
    score_columns = ", ".join([ 
        f"SUM(CASE WHEN s.sub_problem_id = :sub_problem_id_{i} THEN s.score ELSE :param_{i} END) AS score{i}"
        for i in range(1, 32)
    ])
    
    query = f"""
        SELECT u.username, u.total_score,
               {score_columns},
               RANK() OVER (ORDER BY u.total_score DESC, u.final_updated_at ASC) AS rank
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        GROUP BY u.id
        ORDER BY rank
    """
    
    params = {f"sub_problem_id_{i}": i for i in range(1, 32)}
    params.update({f"param_{i}": 0 for i in range(1, 32)})
    
    # 쿼리 실행
    result = db.session.execute(text(query), params)
    
    # 결과를 딕셔너리로 변환
    results_list = []
    rows = result.fetchall()
    
    # 결과 처리
    for row in rows:
        row_list = [row[0], row[1]]  # 사용자 이름과 총점
        row_list.extend([row[i+1] for i in range(1, 32)])  # 각 문제 점수
        row_list.append(row[33])  # 순위
        results_list.append(row_list)
    
    return results_list

# Flask 경로
@app.route("/")
def home():
    # add_users()
    return render_template("index.html")

@app.route("/scores", methods=['GET'])
def scores():
    results_dict = get_user_scores()
    app.logger.info("Scores Data: %s", json.dumps(results_dict, indent=4, ensure_ascii=False))
    return jsonify(results_dict)

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
        if data is None:
            raise ValueError("No JSON data received")
        
        # 로그 출력
        app.logger.info("Received Data: %s", json.dumps(data, ensure_ascii=False))

        # 필요한 정보 추출
        # username = data['username']
        # question = data['question']
        # answer = data['answer']
        username = data.get('username')
        question = data.get('question')
        answer = data.get('answer')

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


# if __name__ == "__main__":
#     app.run(debug=True)
