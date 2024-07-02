from flask import Flask, request, jsonify, render_template
import shutil
from colorama import Fore, Style, init
import ipaddress
import os
import time

app = Flask(__name__)

def subnet_calculator(CIDR_network_ip_address, subnet_count):
    network = ipaddress.IPv4Network(f'{CIDR_network_ip_address}')
    network_portion_plus_subnet = network.prefixlen + (subnet_count - 1).bit_length()
    if network_portion_plus_subnet > 32:
        raise ValueError(f"Cannot divide {network} into {subnet_count} subnets. The required prefix length {network_portion_plus_subnet} is too large.")
    subnets = list(network.subnets(new_prefix=network_portion_plus_subnet))
    return subnets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    network_name = data.get('network_name')
    CIDR_network_ip_address = data.get('CIDR_network_ip_address')
    subnet_count = int(data.get('subnet_count'))
    subnets = subnet_calculator(CIDR_network_ip_address, subnet_count)
    subnet_list = [{
        'network_address': str(subnet.network_address),
        'broadcast_address': str(subnet.broadcast_address),
        'hosts': [str(host) for host in subnet.hosts()]
    } for subnet in subnets[:subnet_count]]
    return jsonify(subnet_list)

if __name__ == '__main__':
    app.run(debug=True)
