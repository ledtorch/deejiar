import os
import json

# Files and sources
JSON_PATH = '../data'

def list_json_files():
    # List all files in the directory
    files = os.listdir(JSON_PATH)
    # Filter out files to only include .json files
    json_files = [file for file in files if file.endswith('.json')]
    return json_files
