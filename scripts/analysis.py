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

def retrieval_analysis(data_path, parameters):
    """
    Process the JSON file based on provided parameters.

    Args:
        data_path (str): Path to the data folder.
        parameters (dict): Parameters for processing.

    Returns:
        dict: Processed data.
    """
    json_file = os.path.join(data_path, 'processed_logs.json')

    # if not os.path.exists(json_file):
    #     raise FileNotFoundError("No processed log file found in the specified directory")

    # # Read the JSON file
    # with open(json_file, 'r') as file:
    #     json_data = json.load(file)

    # # Example processing: filter data based on parameters
    # # Adjust the processing logic as per your requirements
    # filter_key = parameters.get('filter_key')
    # filter_value = parameters.get('filter_value')

    # if filter_key and filter_value:
    #     filtered_data = {
    #         key: value for key, value in json_data.items()
    #         if value.get(filter_key) == filter_value
    #     }
    # else:
    #     filtered_data = json_data  # No filtering applied

    # # Further processing can be done here
    # # For example, aggregating data, calculating statistics, etc.

    # return filtered_data

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
 

