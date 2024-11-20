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


def calculate_cumulative_scores(scores):
    max_scores = []
    min_scores = []
    for k,v in scores.items():
        for i in v:
            max_scores.append(max(i))
            min_scores.append(min(i))
        # else:
        #     print(v)
        #     max_scores.append(max(v))
        #     min_scores.append(min(v))
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot max scores
    ax1.plot(max_scores)
    ax1.set_title('Distribution of Maximum Scores')
    ax1.set_xlabel('Sentences')
    ax1.set_ylabel('Score')
    
    # Plot min scores 
    ax2.plot(min_scores)
    ax2.set_title('Distribution of Minimum Scores')
    ax2.set_xlabel('Sentences')
    ax2.set_ylabel('Score')
    plt.tight_layout()
    return fig
    
def generate_plot(scores, selected_key):
    data_item_mean = None
    data_item_std = None
    data_item = scores[selected_key]
    data_item = np.array(data_item)
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
    plt.tight_layout()
    return fig
    