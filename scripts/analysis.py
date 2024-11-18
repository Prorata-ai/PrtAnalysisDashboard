import pandas as pd
import os
import json
import webbrowser
import tempfile
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, Flask
import os
import sys
import random
import threading
from scripts.process_logs import parse_logs
from scripts.stats_analysis import basic_stats_analysis as basic_analysis

def run_analysis(folder_name, analysis_type):
    """
    Run the selected analysis on the specified data folder
    """
    print(analysis_type)
    data_path = os.path.join('data', folder_name)
    if analysis_type == "show_output":
        return show_output(data_path)
    elif analysis_type == "generate_logs":
        return generate_logs(data_path)
    elif analysis_type == "basic_stats":
        return basic_stats_analysis(data_path)
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")

def retrieval_analysis(data_path):
    def fetch_questions(data_path):
        processed_logs = os.path.join(data_path, 'processed_logs.json')
        with open(processed_logs, 'r') as file:
            data = json.load(file)
        for key, value in data.items():
            print(key, value)

def basic_stats_analysis(data_path,selected_stats):
    figures = basic_analysis(data_path,selected_stats)
    return figures

def generate_logs(data_path):
    print(f"Running generate logs analysis for {data_path}")
    parse_logs(data_path)
    return {"message": "Logs processed successfully!"}

def show_output(data_path):
    print(f"Running output analysis for {data_path}")
    json_file = os.path.join(data_path, 'processed_logs.json')

    if not os.path.exists(json_file):
        return {"message": "No processed log file found in the specified directory"}

    # Read the JSON file
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    random_key = random.choice(list(json_data.keys()))
    sub_keys = list(json_data[random_key].keys())
    # Return the data instead of rendering
    return {
        "json_data": json_data,
        "sub_keys": sub_keys
    }
 

