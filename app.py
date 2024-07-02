from flask import Flask, request, jsonify, render_template
import ipaddress
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        network_name = request.form['networkName']
        CIDR_network_ip_address = request.form['networkIp']
        text_file_yn = request.form['textFile']

        # Validate CIDR format
        try:
            network = ipaddress.IPv4Network(CIDR_network_ip_address)
        except ValueError:
            return jsonify({'error': 'Invalid CIDR format'})

        # Perform subnet calculations based on user input
        if text_file_yn == 'yes':
            subnet_file_content = generate_subnet_text(network_name, CIDR_network_ip_address)
        else:
            subnet_file_content = generate_subnet_text(network_name, CIDR_network_ip_address, create_file=False)

        return jsonify({'result': subnet_file_content})

    except Exception as e:
        return jsonify({'error': str(e)})


def generate_subnet_text(network_name, CIDR_network_ip_address, create_file=True):
    subnets = subnet_calculator(CIDR_network_ip_address)
    subnet_file_content = f"Network Name: {network_name}\n"
    subnet_file_content += f"Network IP Address: {CIDR_network_ip_address}\n\n"

    for i, subnet in enumerate(subnets, start=1):
        subnet_file_content += f"Subnet {i}:\n"
        subnet_file_content += f"Network Address: {subnet.network_address}\n"
        subnet_file_content += f"Broadcast Address: {subnet.broadcast_address}\n"
        subnet_file_content += f"Range of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}\n\n"

    if create_file:
        filename = f"{network_name}_{time.strftime('%Y_%m_%d_%H_%M')}.txt"
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, 'w') as file:
            file.write(subnet_file_content)

    return subnet_file_content


def subnet_calculator(CIDR_network_ip_address):
    network = ipaddress.IPv4Network(CIDR_network_ip_address)
    subnets = list(network.subnets(new_prefix=network.prefixlen))
    return subnets


if __name__ == '__main__':
    app.run(debug=True)
