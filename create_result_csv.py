import os
import pandas as pd
import openai
from main_engine import main as OurChatCompletion
from main_engine import get_general_answer as OpenaiChatCompletion
openai.api_key = "sk-?"


def create_result_csv(question_list_txt, output_csv_path):
    with open(question_list_txt, encoding="utf-8") as fp:
        questions = fp.readlines()

    df = pd.DataFrame({"question":[], "chatbot":[], "ours":[]})
    for question in questions:
        question = question.strip()
        chatbot_result = OpenaiChatCompletion(question)
        ours_result = OurChatCompletion(question)
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
