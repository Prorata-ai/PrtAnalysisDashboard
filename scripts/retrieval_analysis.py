import os
import json
from matplotlib import pyplot as plt

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


def generate_plot(scores, selected_key):
    # Convert scores to float since they appear to be strings
    data = {}
    for kid, key in enumerate(scores[selected_key]):
        data[kid] = float(key)
    
    ks = list(data.keys())
    score_values = list(data.values())
    
    print(ks, score_values)
    fig = plt.figure(figsize=(10, 6))
    plt.plot(ks, score_values, marker='o')  # Added markers to see individual points
    plt.title(f'Retrieval Scores')
    plt.ylabel('Score')
    plt.xlabel('K')
    # plt.grid(True, alpha=0.3)
    # plt.savefig("demo")
    return fig
    