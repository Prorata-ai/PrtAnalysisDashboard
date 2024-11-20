import os
import json
from matplotlib import pyplot as plt
import numpy as np

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
        if v["LLM_question"] not in scores.keys():
            scores[v["LLM_question"]] = []
        if v["LLM_question"] not in texts.keys():    
            texts[v["LLM_question"]] = []  
        score = [float(s) for s in score]
        # print(score)
        scores[v["LLM_question"]].append(score)
        texts[v["LLM_question"]].append(text)
        print(len(scores[v["LLM_question"]])) 
    return scores, texts


def generate_plot(scores, selected_key):
    data_item_mean = None
    data_item_std = None
    data_item = scores[selected_key]
    data_item = np.array(data_item)
    print(data_item.shape)
    if len(data_item)>1:
        data_item_mean = np.mean(data_item, axis=0)
        data_item_std = np.std(data_item, axis=0)
        data_item = data_item_mean
    else:
        data_item = data_item[0]
    print(data_item_std)
    ks = list(range(len(data_item)))
    fig = plt.figure(figsize=(10, 6))
    if data_item_std is not None:
        plt.errorbar(ks, data_item, yerr=data_item_std, marker='o', capsize=5)
    else:
        plt.plot(ks, data_item, marker='o')  # Added markers to see individual points
    plt.title(f'Retrieval Scores')
    plt.ylabel('Score')
    plt.xlabel('K')
    # plt.grid(True, alpha=0.3)
    # plt.savefig("demo")
    return fig
    