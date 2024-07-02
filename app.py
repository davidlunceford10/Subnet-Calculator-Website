from flask import Flask, request, jsonify, render_template
import shutil
from colorama import Fore, Style, init
import ipaddress
import os
import time

app = Flask(__name__)

init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form.get('data')
    # Process data here
    return 'Form submitted successfully'

@app.route('/calculate', methods=['POST'])
def calculate():
    network_name = request.form['networkName']
    CIDR_network_ip_address = request.form['networkIp']
    text_file_yn = request.form['textFile']

    try:
        if text_file_yn == 'yes':
            # Handle file creation and subnet calculation as in your original Python script
            subnet_file_content = f"Network Name: {network_name}\n"
            subnet_file_content += f"Network IP Address: {CIDR_network_ip_address}\n"
            # Perform subnet calculations here and add results to subnet_file_content
        else:
            # Handle subnet calculation without file creation
            subnet_file_content = ""
            # Perform subnet calculations here and add results to subnet_file_content

        return jsonify({'result': subnet_file_content})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
