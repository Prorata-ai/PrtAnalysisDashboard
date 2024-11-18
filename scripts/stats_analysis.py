import json
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import numpy as np

def extract_data(log_data,sel_fields):
    dic = {}
    for k,v in log_data.items():
        if v["LLM_question"] not in dic.keys():
            dic[v["LLM_question"]] = {}
        for f in sel_fields:
            if f not in dic[v["LLM_question"]].keys():
                dic[v["LLM_question"]][f] = []
            if v[f] is not None:
                val = float(v[f].replace('s',''))
            else:
                val = 0.0
            dic[v["LLM_question"]][f].append(val)
    plot_data = {}
    for q in dic.keys():
        sent_data = dic[q]
        plot_data[q] = {}
        for f in sent_data.keys():
            plot_data[q][f] = {"mean":0.0,"std":None}
            field_data = sent_data[f]
            if len(field_data)>1:
                mean = np.mean(field_data)
                std  = np.std(field_data)
            else:
                mean = field_data[0]
                std  = None
            plot_data[q][f]["mean"]=mean
            plot_data[q][f]["std"]=std
    return plot_data

def basic_stats_analysis(data_path, selected_stats):
    """
    Perform basic statistical analysis and generate plots based on selected statistics.

    Args:
        data_path (str): Path to the data directory.
        selected_stats (list): List of statistics to generate plots for.

    Returns:
        list: List of Matplotlib figures corresponding to the generated plots.
    """
    figures = []
    log_json_path = f"{data_path}/processed_logs.json"
    with open(log_json_path, "r") as log_json:
        log_data = json.load(log_json)
    plot_data  = extract_data(log_data,selected_stats)
    plot_stats = {}
    for f in selected_stats:
        means = []
        std = []
        for k,v in plot_data.items():
            means.append(v[f]["mean"])
            std.append(v[f]["std"])
        # Create bar plot for means
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(means))
        # Check if any std values are None
        has_std = all(s is not None for s in std)
        print(std)
        if has_std:
            # Plot with error bars if we have std values
            ax.bar(x, means, yerr=std, capsize=5, alpha=0.8, 
                color='skyblue', ecolor='gray')
        else:
            # Plot just the means if no std values
            ax.bar(x, means, alpha=0.8, color='skyblue')
        # Customize the plot
        ax.set_ylabel(f'{f} (seconds)')
        ax.set_title(f'Mean of {f} time by queries')
        # ax.set_xticks(x)
        # plt.suptitle(f"Time taken: {f} seconds")
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        figures.append(fig)
    
    return figures