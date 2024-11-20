from flask import Flask, render_template, request, jsonify
import os
from scripts.analysis import (
    run_analysis,
    show_output,
    basic_stats_analysis,
    # retrieval_analysis
)
import sys 
import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import uuid
from flask import send_from_directory  # Add this import at the top with other imports
from scripts import process_logs, retrieval_analysis

app = Flask(__name__)

# Configure upload folder
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Define the full list of available statistics once
FULL_AVAILABLE_STATS = [
    "question_condensation","chunk_fetch","chunk_processing",
    "metadata_fetch","node_creation","total_retrieval","refining_time",
    "citation_postprocess","retrive_context","tokenization_duration",
    "source_references","response_duration","total_workflow","attribution_duration",
]
# Add these lines after defining DATA_FOLDER and FULL_AVAILABLE_STATS
TEMP_IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_images')
os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Get list of available data folders
    data_folders = [f for f in os.listdir(DATA_FOLDER) 
                   if os.path.isdir(os.path.join(DATA_FOLDER, f))]
    
    # Get list of available analysis scripts
    available_analyses = [
        "generate_logs",
        "show_output",
        "basic_stats",
        "retrieval_analysis",
        # "advanced_analysis"
        # Add more analysis types as needed
    ]    
    return render_template('index.html', 
                         data_folders=data_folders,
                         analyses=available_analyses)

@app.route('/show_output/<folder_name>')
def show_output_analysis(folder_name):
    data_path = os.path.join('data', folder_name)
    try:
        result = show_output(data_path)
        # Access the correct keys from the result dictionary
        return render_template('show_output.html', 
                             json_str=json.dumps(result["json_data"], default=str),
                             sub_keys_str=json.dumps(result["sub_keys"]))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/basic_stats/<folder_name>', methods=['GET', 'POST'])
def basic_stats_page(folder_name):
    if request.method == 'GET':
        return render_template('basic_stats.html', 
                               available_stats=FULL_AVAILABLE_STATS,
                               folder_name=folder_name)
    data = request.get_json()
    selected_stats = data.get('selected_stats', [])
    try:
        data_path = os.path.join(DATA_FOLDER, folder_name)
        # Generate plots and save them to TEMP_IMAGE_FOLDER
        figures = basic_stats_analysis(data_path, selected_stats)
        encoded_images = []
        for fig in figures:
            buf = BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            encoded_images.append(image_base64)
            plt.close(fig)  # Close the figure after encoding to free memory
        return jsonify({'success': True, 'plot_images': encoded_images}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/retrieval_analysis/<folder_name>', methods=['GET', 'POST'])
def retrieval_analysis_page(folder_name):
    data_path = os.path.join(DATA_FOLDER, folder_name)
    scores,texts = retrieval_analysis.retrieve_questions(data_path)
    
    if request.method == 'GET':
        return render_template('retrieval_analysis.html', folder_name=folder_name)
    
    data = request.get_json()
    analysis_type = data.get('analysis_type')
    sub_option = data.get('sub_option')
    selected_key = data.get('selected_key') 
    
    if analysis_type == "individual":
        if sub_option == "score" and not selected_key:
            try:
                keys = list(scores.keys())
                return jsonify({
                    'success': True,
                    'results': {
                        'analysis_type': 'individual',
                        'keys': keys
                    }
                }), 200
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400

        elif sub_option == "score" and selected_key:
            try:
                # Generate plot for the selected_key
                fig = retrieval_analysis.generate_plot(scores, selected_key)
                # Convert the matplotlib figure to a base64-encoded string
                buf = BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                plt.close(fig)  # Close the figure to free memory
                
                return jsonify({
                    'success': True,
                    'plot_image': image_base64
                }), 200
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400

    elif analysis_type == "cumulative":
        try:
            stats = retrieval_analysis.compute_cumulative_stats(scores)
            return jsonify({
                'success': True,
                'results': {
                    'analysis_type': 'cumulative',
                    'stats': stats
                }
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    return jsonify({"message": "Invalid analysis type"}), 400
    
@app.route('/download_image/<folder_name>/<key>', methods=['GET'])
def download_image(folder_name, key):
    try:
        # Construct the filename and path
        filename = f"{key}.png"
        file_path = os.path.join(TEMP_IMAGE_FOLDER, filename)
        
        # Check if the file exists
        if os.path.exists(file_path):
            return send_from_directory(TEMP_IMAGE_FOLDER, filename, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'Image not found.'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@app.route('/run_analysis', methods=['POST'])
def analyze():
    data = request.get_json()
    folder_name = data.get('folder')
    analysis_type = data.get('analysis_type')
    try:
        if analysis_type == "generate_logs":
            try:
                process_logs.parse_logs(folder_name)
                return jsonify({
                        "success": True,
                        "results": {
                            "message": f"Logs generated successfully for {folder_name}"
                        }
                    }), 200
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 400
            
        if analysis_type == "show_output":
            return jsonify({
                'success': True, 
                'results': {
                    'redirect_url': f'/show_output/{folder_name}',
                    'new_tab': True
                }
            }), 200
        elif analysis_type=="basic_stats":
            return jsonify({
                'success': True, 
                'results': {
                    'redirect_url': f'/basic_stats/{folder_name}',
                    'new_tab': True
                }
            }), 200
        elif analysis_type == "retrieval_analysis":
            return jsonify({
                'success': True, 
                'results': {
                    'redirect_url': f'/retrieval_analysis/{folder_name}',
                    'new_tab': True
                }
            }), 200
          
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)