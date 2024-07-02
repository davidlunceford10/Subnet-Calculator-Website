from flask import Flask, render_template, request, jsonify
import ipaddress
import shutil
import time

app = Flask(__name__)

# Initialize Colorama (optional for web app)

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

    output.append(center_text(color_text('Fixed Length Subnet Mask Subnetting Calculator', Fore.GREEN)))
    output.append(f'\nNetwork Name: {network_name}\n')

    subnet_number = 0
    for subnet in subnets:
        subnet_number += 1
        output.append(f'\nSubnet {subnet_number}:')
        output.append(f'Network Address: {subnet.network_address}')
        output.append(f'Broadcast Address: {subnet.broadcast_address}')
        output.append(f'Range of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}')

    output_text = '\n'.join(output)
    return output_text

def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    centered_text = text.center(terminal_width)
    return centered_text

if __name__ == "__main__":
    app.run(debug=True)
