import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding
from similarity import euclidean_distance_similarity, cosine_similarity, adjusted_cosine_similarity

openai.api_key = "sk-?"


def search_db(search_embeddings, csv_path, topk=5) -> dict:
    ''' 对单个dataframe里的进行搜索 '''
    df = pd.read_csv(csv_path, encoding="ANSI")
    # print(df)
    df["embedding"] = df["embedding"].apply(eval).apply(np.array)

    df["similarity"] = df["embedding"].apply(
        lambda x: cosine_similarity(x, search_embeddings)
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


def main(question, csv_path=r"data\book\400_emb.csv"):
    search_embeddings = get_embedding(question, engine="text-embedding-ada-002")
    candidate_answers = search_db(search_embeddings, csv_path, 5)
    prompt = get_prompt(list(candidate_answers.keys()), question)
    response = get_general_answer(prompt)
    return response


if __name__ == '__main__':
    question = "月经多少天来一次正常？"
    response = main(question)
    print(response)
