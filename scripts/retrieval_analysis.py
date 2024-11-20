import os
import json

def retrieve_questions(data_path):
    json_file = os.path.join(data_path, 'processed_logs.json')
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    scores = {}
    texts = {}
    for k,v in json_data.items():
        score = []
        text = []
        for rk,rv in v["retrievals"].items():
            score.append(rv["score"])
            text.append(rv["text"])
        scores[v["LLM_question"]] = score
        texts[v["LLM_question"]] = text
    return scores, texts


def individual_plots(data):
    return None