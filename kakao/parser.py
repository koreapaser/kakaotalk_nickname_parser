from typing import Optional

import pandas as pd
from pandas import DataFrame


MAX_MESSAGE_LEN = 3
VALID_CODE_LEN = 8
ADMIN_USERS = [
    "주식방 고파파",
    "주식초보 고파파(6b8fd5b5)",
]


def is_korean(target: str):
    for each in target:
        if '가' <= each <= '힣':
            return True
    return False


def is_hexadecimal(target: str):
    for each in target:
        if not (('0' <= each <= '9') or ('a' <= each <= 'f') or ('A' <= each <= 'F')):
            return False
    return True


def is_valid_code(target: str):
    if not target:
        return False
    return is_hexadecimal(target) and len(target) == VALID_CODE_LEN


def remove_korean(target: str) -> str:
    st_idx = -1
    for idx, each in enumerate(target):
        if '가' <= each <= '힣':
            st_idx = idx
            break
    if st_idx == -1:
        return target

    ed_idx = -1
    for idx, each in enumerate(reversed(target)):
        if '가' <= each <= '힣':
            ed_idx = len(target) - 1 - idx
            break

    if st_idx == 0:
        first = ''
    else:
        first = target[:st_idx]
    if ed_idx == (len(target) - 1):
        second = ''
    else:
        second = target[ed_idx + 1:]
    return first + second


def get_code(nickname: str) -> Optional[str]:
    nickname = remove_korean(nickname)
    if not nickname:
        return None

    splited = None
    if '(' in nickname:
        splited = nickname.split('(')
    elif ')' in nickname:
        splited = nickname.split(')')
    elif '[' in nickname:
        splited = nickname.split('[')
    elif ']' in nickname:
        splited = nickname.split(']')
    elif ' ' in nickname:
        splited = nickname.split(' ')
    elif '.' in nickname:
        splited = nickname.split('.')
    elif '/' in nickname:
        splited = nickname.split('/')

    if splited:
        candidates = []
        for each in splited:
            code = get_code(each)
            if code is not None:
                candidates.append(code)
        if len(candidates) > 1:
            valid_candidates = []
            for each_candidate in candidates:
                if is_valid_code(each_candidate):
                    valid_candidates.append(each_candidate)
            if len(valid_candidates) > 1:
                assert False, f"valid_candidates=[{valid_candidates}]"
            elif len(valid_candidates) == 1:
                return valid_candidates[0]
            elif len(valid_candidates) == 0:
                # print(f"len(valid_candidates) == 0, candidates=[{candidates}]")
                return None
        elif len(candidates) == 1:
            return candidates[0]
        return None
    elif not is_korean(nickname):
        return nickname


def parse_csv(csv_path: str):
    df: DataFrame = pd.read_csv(csv_path)
    users = {}
    for i in range(0, df.shape[0]):
        current_user = df.User[i]
        current_message = df.Message[i]
        if current_message.endswith('님이 들어왔습니다.'):
            if current_user in users:
                users[current_user]['out'] = False
                users[current_user]['blocked'] = False
        if current_message.endswith('님이 나갔습니다.'):
            if current_user not in users:
                users[current_user] = {
                    'out': True,
                    'messages': [],
                }
            users[current_user]['out'] = True
        if df.User[i] in ADMIN_USERS and current_message.endswith('님을 내보냈습니다.'):
            kicked_user = current_message[:len(current_message) - len('님을 내보냈습니다.')]
            if kicked_user in users:
                users[kicked_user]['out'] = True
                users[kicked_user]['blocked'] = True
            continue
        if current_user not in users:
            users[current_user] = {
                'out': False,
                'messages': [],
            }
        if len(users[current_user]['messages']) >= MAX_MESSAGE_LEN:
            users[current_user]['messages'].pop(0)
        users[current_user]['messages'].append({
            'content': current_message,
            'date': df.Date[i],
        })
    return users
