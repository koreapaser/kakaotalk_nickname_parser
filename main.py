import json
import os

from kakao.parser import get_code, parse_csv, ADMIN_USERS, is_valid_code, MAX_MESSAGE_LEN


if __name__ == '__main__':
    if not os.path.exists('parsed.json'):
        users = parse_csv("KakaoTalk_Chat_고파스 공식 주식방_2020-09-21-19-24-53.csv")
        with open('parsed.json', 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    unique_codes = {}
    idx = 1
    with open('parsed.json', 'r') as f:
        parsed = json.load(f)
        for nickname, val in parsed.items():
            if val['out']:
                continue
            if nickname in ADMIN_USERS:
                continue
            code = get_code(nickname)
            if not is_valid_code(code):
                print(f"[{idx}]: not valid code")
                print(f"nickname=[{nickname}], captured_code=[{code}]")
                print("")
                idx += 1
                continue
            if code in unique_codes:
                print(f"[{idx}]: duplicated code")
                print(f"nickname=[{nickname}], code=[{code}]")
                print(f"최근 [{MAX_MESSAGE_LEN}]개 메시지")
                for message in val['messages']:
                    print(f"[{nickname}]({message['date']}): {message['content']}")
                print(f"nickname=[{unique_codes[code]['nickname']}]")
                for message in unique_codes[code]['messages']:
                    print(f"[{unique_codes[code]['nickname']}]({message['date']}): {message['content']}")
                print("")
                idx += 1
                continue
            unique_codes[code] = val
            unique_codes[code]['nickname'] = nickname
