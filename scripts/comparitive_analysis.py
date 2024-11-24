import os
import json

def new_dict(log):
    sents = {}
    for key, value in log.items():
        if value["LLM_question"] not in sents.keys():
            sents[value["LLM_question"]] = [value]
        else:
            sents[value["LLM_question"]].append(value)
    return sents

def comparison_logs(folder1, folder2):
    with open(os.path.join(f"data/{folder1}", "processed_logs.json"), "r") as f:
        log1 = json.load(f)
    new_log1 = new_dict(log1)
    with open(os.path.join(f"data/{folder2}", "processed_logs.json"), "r") as f:
        log2 = json.load(f)
    new_log2 = new_dict(log2)

    common_queries = list(set(new_log1.keys()) & set(new_log2.keys()))
    
    comparisons = {}
    for query in common_queries:
        v1 = new_log1[query]
        v2 = new_log2[query]
        comparisons[query] = {
            "model1": v1,
            "model2": v2
        }
    
    return comparisons

def compare_outputs(comparitive_logs):
    query_list = []
    model1 = []
    model2 = []
    for query, values in comparitive_logs.items():
        max_count = max(len(values["model1"]), len(values["model2"]))
        for i in range(max_count):
            query_list.append(query)
            model1_entry = values["model1"][i]["LLM_answer"] if i < len(values["model1"]) else " "
            model2_entry = values["model2"][i]["LLM_answer"] if i < len(values["model2"]) else " "
            model1.append(model1_entry)
            model2.append(model2_entry)
    
    return query_list, model1, model2