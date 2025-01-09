import requests
import json

def chat(question):
    payload = {
        "model": "llama3.2:3b",
        "prompt": question
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=10000)
    # print(f'response.text={response.text}')

    items = response.text.strip().split('\n')
    # print('items=', items)

    tokens = []
    for item in items:
        # print('item=', item)
        o = json.loads(item)
        tokens.append(o['response'])

    response_text = ' '.join(tokens)
    return response_text

if __name__ == '__main__':
    print(chat("法國的首都在哪裡？"))

