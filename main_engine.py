import pandas as pd
import numpy as np
import json
import requests
import openai
from openai.embeddings_utils import get_embedding
from similarity import euclidean_distance_similarity, cosine_similarity, adjusted_cosine_similarity

openai.api_key = "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"


def search_db(search_embeddings, csv_path, similarity_method=cosine_similarity, topk=5) -> dict:
    ''' 对单个dataframe里的进行搜索 '''
    df = pd.read_csv(csv_path, encoding="ANSI")
    # print(df)
    df["embedding"] = df["embedding"].apply(eval).apply(np.array)

    df["similarity"] = df["embedding"].apply(
        lambda x: similarity_method(x, search_embeddings)
    )

    results = df.sort_values("similarity", ascending=False).head(topk)
    candidate_answers = {}
    # {"大姨妈知识点1": 0.49, "知识点2": 0.40}
    for index, row in results.iterrows():
        candidate_answers[row["text"]] = float(row["similarity"])

    return candidate_answers


def get_prompt(content_list, question):
    prompt = f'''
    给定的参考信息为:{content_list}
    你是一个生理课老师，收到了处在青春期的女学生的一个问题：{question}
    如果参考信息中没有内容能作为依据回答问题请返回“对不起，我无法提供相关具体信息，因为我的知识库中并没有包含这方面的信息。”，如果参考信息中存在内容能作为依据回答问题，请温和亲切地回答该问题。请注意，必须按照参考信息提供的内容进行回答，不得进行任何增删改。
    '''
    return prompt


def get_general_answer(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": content
        }]
    )
    if "choices" not in response:
        return "Error"
    else:
        return response["choices"][0]["message"]["content"]


def main(question, csv_path=r"data\book\400_gpt35_emb.csv", similarity_method=cosine_similarity):
    search_embeddings = get_embedding(question, engine="text-embedding-ada-002")
    candidate_answers = search_db(search_embeddings, csv_path, similarity_method, 5)
    prompt = get_prompt(list(candidate_answers.keys()), question)
    response = get_general_answer(prompt)
    return response

#----------------------------------------------- Baidu Ernie ------------------------------------------------
ERNIE_API_KEY = "manSsMGCFYGDbIVwfqaCuVQs"
ERNIE_SECRET_KEY = "4Z7P1VPcH2m0P2qPR24NO7ixAqpRmued"
ERNIE_ACCESS_TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
ERNIE_EMBEDDING_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token="
ERNIE_CHAT_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="
ERNIE_HEADERS = {'Content-Type': 'application/json'}
def get_ernie_embedding(search_term):
    payload = json.dumps({
        "input": [search_term]
    })
    response = requests.request("POST", ERNIE_EMBEDDING_URL + get_ernie_access_token(),
                                headers=ERNIE_HEADERS, data=payload)
    print(response.text)
    return list(eval(response.text)["data"][0]["embedding"])

def get_ernie_general_answer(content):
    payload = {"messages":
        [{
            "role": "user",
            "content": content
        }]
    }
    response = requests.request("POST", ERNIE_CHAT_URL + get_ernie_access_token(), headers=ERNIE_HEADERS, data=json.dumps(payload))
    output = json.loads(response.text)
    return output["result"]

def get_ernie_access_token():
    params = {"grant_type": "client_credentials", "client_id": ERNIE_API_KEY, "client_secret": ERNIE_SECRET_KEY}
    return str(requests.post(ERNIE_ACCESS_TOKEN_URL, params=params).json().get("access_token"))

def main_ernie(question, csv_path=r"data/book/400_ernie_emb.csv", similarity_method=cosine_similarity):
    search_embeddings = get_ernie_embedding(question)
    print(search_embeddings)
    candidate_answers = search_db(search_embeddings, csv_path, 5)
    prompt = get_prompt(list(candidate_answers.keys()), question)
    response = get_ernie_general_answer(prompt)
    return response



if __name__ == '__main__':
    question = "月经多少天来一次正常？"
    response = main_ernie(question)
    print(response)
