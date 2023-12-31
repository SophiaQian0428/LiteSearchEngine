import inspect, re
import pandas as pd
import openai
from main_engine import main as OurChatCompletionGPT35
from main_engine import main_ernie as OurChatCompletionERNIE
from main_engine import get_general_answer as OpenaiChatCompletion
from similarity import euclidean_distance_similarity, cosine_similarity, adjusted_cosine_similarity

OurChatCompletionGPT35EDS = lambda text: OurChatCompletionGPT35(text, similarity_method=euclidean_distance_similarity)
OurChatCompletionGPT35CS = lambda text: OurChatCompletionGPT35(text, similarity_method=cosine_similarity)
OurChatCompletionGPT35ACS = lambda text: OurChatCompletionGPT35(text, similarity_method=adjusted_cosine_similarity)

OurChatCompletionERNIEEDS = lambda text: OurChatCompletionERNIE(text, similarity_method=euclidean_distance_similarity)
OurChatCompletionERNIECS = lambda text: OurChatCompletionERNIE(text, similarity_method=cosine_similarity)
OurChatCompletionERNIEACS = lambda text: OurChatCompletionERNIE(text, similarity_method=adjusted_cosine_similarity)


last_key_idx = 0
key_list = [
    #TODO
]
openai.api_key = key_list[last_key_idx]

def switch_api_key():
    global last_key_idx
    current_key_idx = (last_key_idx+1) % len(key_list)
    openai.api_key = key_list[current_key_idx]
    last_key_idx = current_key_idx


def call_chat_if_fail(text, chat_completion_method, results=[]):
    try:
        result = chat_completion_method(text)
        if result == "Error":
            return True
        else:
            results.append(result)
            return False
    except Exception as e:
        print(e)
        return True


def create_result_csv(question_list_txt, output_csv_path):
    with open(question_list_txt, encoding="utf-8") as fp:
        questions = fp.readlines()

    df = pd.DataFrame({"question":[], "result_a":[], "result_b":[]})
    method_a = OurChatCompletionGPT35CS
    method_b = OurChatCompletionGPT35EDS
    for question in questions:
        question = question.strip()

        results = []
        while call_chat_if_fail(question, method_a, results):
            switch_api_key()
        result_a = results[0]

        results = []
        while call_chat_if_fail(question, method_b, results):
            switch_api_key()
        result_b = results[0]

        print(f"[QUESTION] {question}")
        print(f"[{method_a.__name__}] {result_a}")
        print(f"[{method_b.__name__}] {result_b}")
        print(f"=========================")
        df.loc[len(df.index)] = [question, result_a, result_b]

    df.to_csv(output_csv_path, encoding="ANSI", index = False)


if __name__ == '__main__':
    question_list_txt = r"data\question\question_list_1.txt"
    output_csv_path = r"test\question_list_1_CS_EDS.csv"
    create_result_csv(question_list_txt, output_csv_path)
