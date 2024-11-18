import requests
import json
import time
import os
import sys
import argparse
import time
import random
import argparse
import re
import ast


def string_to_dict(node_str):
    input_str = node_str.strip()[9:-1]
    # Initialize variables for parsing
    result = {}
    key, value = None, None
    bracket_count = 0
    in_quotes = False
    part = []
    
    # Helper function to process and clean up key-value pairs
    def process_key_value(key, value):
        key = key.strip()
        value = value.strip()
        
        # Handle different types of values
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]  # Strip surrounding quotes
        elif value == 'None':
            value = None
        elif value.startswith("{") and value.endswith("}"):
            try:
                value = eval(value)  # Convert string representation of dict
            except:
                pass
        elif value.startswith("[") and value.endswith("]"):
            try:
                value = eval(value)  # Convert string representation of list
            except:
                pass
        return key, value

    # Parse the input string character by character
    for i, char in enumerate(input_str):
        if char == "'" and (i == 0 or input_str[i-1] != "\\"):  # Toggle in_quotes status
            in_quotes = not in_quotes
        elif char in ("(", "{"):
            bracket_count += 1
        elif char in (")", "}"):
            bracket_count -= 1

        if char == "," and bracket_count == 0 and not in_quotes:
            # Process the accumulated part
            if "=" in part:
                key, value = "".join(part).split("=", 1)
                key, value = process_key_value(key, value)
                result[key] = value
            part = []
        else:
            part.append(char)
    
    # Process the last key-value pair
    if part:
        if "=" in part:
            key, value = "".join(part).split("=", 1)
            key, value = process_key_value(key, value)
            result[key] = value

    return result

def retrieved_nodes(nodes_str):
    node_pattern = r"NodeWithScore\(node=(.*?), score=(.*?)\)"
    matches = re.findall(node_pattern, nodes_str, re.DOTALL)
    results = {}
    for match in matches:
        node_str, score = match
        dict_ = string_to_dict(node_str)
        metadata = dict_["metadata"]
        results[dict_["id_"]] = {
            "text": dict_["text"],
            "score": score,
            "metadata": metadata,
        }
    return results

def parse_events(events):
    question_condensation = None
    chunk_fetch = None
    chunk_processing = None
    metadata_fetch = None
    node_creation = None
    total_retrieval = None
    refining_time = None
    citation_postprocess = None
    retrive_context = None
    tokenization_duration = None
    source_references = None
    response_duration = None
    total_workflow = None
    attribution_duration = None
    LLM_question = None
    LLM_answer = None
    LLM_query = None
    # retrieval_query = None
    retrievals = {}

    for event in events:
        # if "RetrievalEnd query:" in event:
        #     retrieval_query = event.split("RetrievalEnd query: ")[1].strip()
        if "RetrievalEnd nodes:" in event:
            nodes_str = event.split("RetrievalEnd nodes: ")[1].strip()

    retrievals = retrieved_nodes(nodes_str)        

    for event in events:
        if "Span completed: CondensePlusContextChatWorkflow.CondenseQuestionStep" in event:
            question_condensation = event.split("Duration: ")[1].strip()
        elif "Span completed: index_retriever.search_api_call" in event:
            chunk_fetch = event.split("Duration: ")[1].strip()
        elif "Span completed: index_retriever.process_chunks " in event:
            chunk_processing = event.split("Duration: ")[1].strip()
        elif "Span completed: index_retriever.fetch_metadata" in event:
            metadata_fetch = event.split("Duration: ")[1].strip()
        elif "Span completed: index_retriever.create_nodes" in event:
            node_creation = event.split("Duration: ")[1].strip()
        elif "Span completed: BaseRetriever.aretrieve" in event:
            total_retrieval = event.split("Duration: ")[1].strip()
        elif "Span completed: BaseRetriever.aretrieve" in event:
            refining_time = event.split("Duration: ")[1].strip()
        elif "Span completed: CitationSourceNodePostprocessor._postprocess_nodes" in event:
            citation_postprocess = event.split("Duration: ")[1].strip()
        elif "Span completed: CondensePlusContextChatWorkflow.RetrieveContextStep" in event:
            retrive_context = event.split("Duration: ")[1].strip()
        elif "Span completed: TokenTextSplitter.split_text-" in event:
            tokenization_duration = event.split("Duration: ")[1].strip()
        elif "Span completed: get_source_references" in event:
            source_references = event.split("Duration: ")[1].strip()
        elif "Span completed: CondensePlusContextChatWorkflow.SynthesizeResponseStep" in event:
            response_duration = event.split("Duration: ")[1].strip()
        elif  "Span completed: Workflow.run" in event:
            total_workflow = event.split("Duration: ")[1].strip()
        elif "Span completed: handle_attributions" in event:
            attribution_duration = event.split("Duration: ")[1].strip()
        elif "LLMChatEnd response:" in event:
            LLM_answer = event.split("assistant: ")[1].strip()    
        elif "LLMChatEnd last message:" in event:
            LLM_question = event.split("last message: ")[1].strip()
        elif "RetrievalStart query:" in event:
            LLM_query = event.split("RetrievalStart query: ")[1].strip()
    results = {
        "LLM_question": LLM_question,
        "LLM_answer": LLM_answer,
        "LLM_query": LLM_query,
        # "retrieval_query": retrieval_query,
        "retrievals": retrievals,
        "question_condensation": question_condensation,
        "chunk_fetch": chunk_fetch,
        "chunk_processing": chunk_processing,
        "metadata_fetch": metadata_fetch,
        "node_creation": node_creation,
        "total_retrieval": total_retrieval,
        "refining_time": refining_time,
        "citation_postprocess": citation_postprocess,
        "retrive_context": retrive_context, 
        "tokenization_duration": tokenization_duration,
        "source_references": source_references,
        "response_duration": response_duration,
        "total_workflow": total_workflow,
        "attribution_duration": attribution_duration
        }
    return results

def parse_logs(log_dir):
    processed_logs = {}
    for l in os.listdir(f"{log_dir}/thread_logs"):
        results = parse_events(open(f"{log_dir}/thread_logs/{l}", "r").readlines())
        processed_logs[l] = results
    with open(f"{log_dir}/processed_logs.json", "w") as f:
        json.dump(processed_logs, f, indent=4)
