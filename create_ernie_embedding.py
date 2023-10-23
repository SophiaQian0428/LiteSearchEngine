import os
import csv
import json
import requests

entries = []

ERNIE_API_KEY = ""
ERNIE_SECRET_KEY = ""
ERNIE_ACCESS_TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
ERNIE_EMBEDDING_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token="
ERNIE_CHAT_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="
ERNIE_HEADERS = {'Content-Type': 'application/json'}


def get_ernie_access_token():
    params = {"grant_type": "client_credentials", "client_id": ERNIE_API_KEY, "client_secret": ERNIE_SECRET_KEY}
    return str(requests.post(ERNIE_ACCESS_TOKEN_URL, params=params).json().get("access_token"))


def get_ernie_embedding(search_term):
    payload = json.dumps({
        "input": [search_term]
    })
    response = requests.request("POST", ERNIE_EMBEDDING_URL + get_ernie_access_token(),
                                headers=ERNIE_HEADERS, data=payload)
    # print(response.text)
    return list(eval(response.text)["data"][0]["embedding"])


def call_api_if_fail(text, embs=[]):
    try:
        emb = get_ernie_embedding(text)
        embs.append(emb)
    except Exception as e:
        print(f"ERROR:{e}")
        return True
    return False


def convert_txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r', encoding="utf-8") as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open(csv_file_path, 'w', encoding="ANSI") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('text', 'embedding'))
            writer.writerows(lines)


def create_embedding_from_txt(source_txt_path, output_csv_path):
    output_txt_path = f"{os.path.splitext(output_csv_path)[0]}.txt"
    output_fp = open(output_txt_path, "a+", encoding="utf-8")

    global entries
    if os.path.isfile(f"{source_txt_path}.tmp"):
        with open(f"{source_txt_path}.tmp", encoding="utf-8") as source_fp:
            entries = source_fp.readlines()
    else:
        with open(source_txt_path, encoding="utf-8") as source_fp:
            entries = source_fp.readlines()

    while entries:
        embs = []
        text = entries[0].strip()
        while call_api_if_fail(text, embs):
            pass
        emb = embs[0]
        print(f"{text}\t{emb}")
        output_fp.write(f"{text}\t{emb}\n")
        entries.pop(0)
    output_fp.close()

    convert_txt_to_csv(output_txt_path, output_csv_path)


if __name__ == '__main__':
    source_txt_path = r"data\book\400.txt"
    output_csv_path = r"data\book\400_ernie_emb.csv"
    try:
        create_embedding_from_txt(source_txt_path, output_csv_path)
    except KeyboardInterrupt:
        with open(f"{source_txt_path}.tmp", encoding="utf-8") as fp:
            fp.writelines(entries)
        fp.close()
