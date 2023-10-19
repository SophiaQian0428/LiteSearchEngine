import os
import pandas as pd
import openai
from main_engine import main as OurChatCompletion
from main_engine import get_general_answer as OpenaiChatCompletion

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

    df = pd.DataFrame({"question":[], "chatbot":[], "ours":[]})
    for question in questions:
        question = question.strip()

        results = []
        while call_chat_if_fail(question, OpenaiChatCompletion, results):
            switch_api_key()
        chatbot_result = results[0]

        results = []
        while call_chat_if_fail(question, OurChatCompletion, results):
            switch_api_key()
        ours_result = results[0]

        print(f"[QUESTION] {question}")
        print(f"[CHATBOT] {chatbot_result}")
        print(f"[OURS] {ours_result}")
        print(f"=========================")
        df.loc[len(df.index)] = [question, chatbot_result, ours_result]

    df.to_csv(output_csv_path, encoding="ANSI")


if __name__ == '__main__':
    question_list_txt = r"data\question\question_list_1.txt"
    output_csv_path = r"test\question_list_1.csv"
    create_result_csv(question_list_txt, output_csv_path)
