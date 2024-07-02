from flask import Flask, render_template, request, jsonify
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        network_name = request.form['networkName']
        CIDR_network_ip_address = request.form['networkIp']
        subnet_count = int(request.form['subnetCount'])

        subnets = subnet_calculator(CIDR_network_ip_address, subnet_count)

        result = format_subnets(network_name, subnets)

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})

def subnet_calculator(CIDR_network_ip_address, subnet_count):
    network = ipaddress.IPv4Network(CIDR_network_ip_address)

    network_portion_plus_subnet = network.prefixlen + (subnet_count - 1).bit_length()

    if network_portion_plus_subnet > 32:
        raise ValueError(f"Cannot divide {network} into {subnet_count} subnets. The required prefix length {network_portion_plus_subnet} is too large.")

    subnets = list(network.subnets(new_prefix=network_portion_plus_subnet))

    return subnets

def format_subnets(network_name, subnets):
    output = []

    output.append(f'Fixed Length Subnet Mask Subnetting Calculator\n')
    output.appe
