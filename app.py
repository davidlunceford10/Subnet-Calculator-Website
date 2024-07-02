from flask import Flask, request, jsonify, render_template
import ipaddress
import os
import time
import shutil
from colorama import Fore, Style, init

app = Flask(__name__)

init()

# Function to calculate subnets
def subnet_calculator(CIDR_network_ip_address, subnet_count):
    try:
        network = ipaddress.IPv4Network(CIDR_network_ip_address)
        network_portion_plus_subnet = network.prefixlen + (subnet_count - 1).bit_length()

        if network_portion_plus_subnet > 32:
            raise ValueError(f"Cannot divide {network} into {subnet_count} subnets. The required prefix length {network_portion_plus_subnet} is too large.")

        subnets = list(network.subnets(new_prefix=network_portion_plus_subnet))

        return subnets

    except ValueError as e:
        return str(e)

# Function to handle form submission and subnet calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        network_name = request.form['networkName']
        CIDR_network_ip_address = request.form['networkIp']
        text_file_yn = request.form['textFile']

        if text_file_yn == 'yes':
            subnet_file_content = f"Network Name: {network_name}\n"
            subnet_file_content += f"Network IP Address: {CIDR_network_ip_address}\n"

            subnets = subnet_calculator(CIDR_network_ip_address, int(request.form['subnetCount']))
            if isinstance(subnets, list):
                subnet_file_content += '\n'.join([f'Subnet {i+1}:\nNetwork Address: {subnet.network_address}\nBroadcast Address: {subnet.broadcast_address}\nRange of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}\n' for i, subnet in enumerate(subnets)])
            else:
                subnet_file_content += f'Error: {subnets}'

        else:
            subnets = subnet_calculator(CIDR_network_ip_address, int(request.form['subnetCount']))
            if isinstance(subnets, list):
                subnet_file_content = '\n'.join([f'Subnet {i+1}:\nNetwork Address: {subnet.network_address}\nBroadcast Address: {subnet.broadcast_address}\nRange of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}\n' for i, subnet in enumerate(subnets)])
            else:
                subnet_file_content = f'Error: {subnets}'

        return jsonify({'result': subnet_file_content})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
