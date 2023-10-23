import os
import openai
from openai.embeddings_utils import get_embedding
import csv

entries = []

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


def call_api_if_fail(text, embs=[]):
    try:
        emb = get_embedding(text, engine="text-embedding-ada-002")
        embs.append(emb)
    except Exception as e:
        print(e)
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
            switch_api_key()
        emb = embs[0]
        print(f"{text}\t{emb}")
        output_fp.write(f"{text}\t{emb}\n")
        entries.pop(0)
    output_fp.close()

    convert_txt_to_csv(output_txt_path, output_csv_path)


if __name__ == '__main__':
    source_txt_path = r"data\book\400.txt"
    output_csv_path = r"data\book\400_gpt35_emb.csv"
    try:
        create_embedding_from_txt(source_txt_path, output_csv_path)
    except KeyboardInterrupt:
        with open(f"{source_txt_path}.tmp", encoding="utf-8") as fp:
            fp.writelines(entries)
        fp.close()
