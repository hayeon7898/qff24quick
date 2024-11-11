def parse_question(question: str) -> tuple:
    # 숫자와 문자를 분리
    lab = int(question[0] )# 첫 번째 문자가 lab 번호
    type_id = f'lab{lab}'

    part = question[1]      # 두 번째 문자가 문제 세부 번호 (a, b, c, d 등)

    # 문제 번호 범위 설정
    if lab == 1:
        base_number = 1
    elif lab == 2:
        base_number = 5
    elif lab == 3:
        base_number = 9
    elif lab == 4:
        base_number = 15
    elif lab == 5:
        base_number = 23
    elif lab == 6:
        base_number = 27
    else:
        raise ValueError("Lab 번호는 1~6 사이여야 합니다.")
    
    # 세부 번호에 따라 문제 번호 결정
    # 'a'의 ASCII 코드가 97이므로 이를 기준으로 인덱스 계산
    problem_number = base_number + (ord(part) - ord('a'))
    
    # 결과 출력
    return type_id, problem_number

# 테스트
#print(parse_question("3e"))  # 출력: ('lab1', 1)
#print(parse_question("4f"))  # 출력: ('lab4', 14)
