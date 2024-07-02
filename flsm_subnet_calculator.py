import shutil
from colorama import Fore, Style, init
import ipaddress
import os
import time


def main():

    init()

    print(center_text(color_text('Fixed Length Subnet Mask Subnetting Calculator', Fore.GREEN)))

    #Name the network and enter CIDR notation IP address
    network_name = input(color_text('What is the name of your network? ', Fore.CYAN))
    CIDR_network_ip_address = input((color_text('What is the network ip address in CIDR notation? (i.e. 192.168.1.0/24): ', Fore.CYAN)))

    #Asks if user wants a document of their subnets and de-capitalizes the user input
    text_file_yn = input(color_text('Do you want a text copy of your subnets? (Y/N) ', Fore.LIGHTYELLOW_EX))
    text_file_yn = text_file_yn.lower()

    #Verifies that user input is either a lowercase y or n
    while text_file_yn not in  ['y', 'n']:
        print(color_text('That is not a valid input.', Fore.RED))
        time.sleep(1.5)
        text_file_yn = input(color_text('Do you want a text copy of your subnets? (Y/N) ', Fore.LIGHTYELLOW_EX))
        text_file_yn.lower()

    #Writes the subnets from the subnet calculator to a text file named by the user and prints the output to the terminal. Handles errors with an exception for incorrect user input.
    if text_file_yn == 'y': 
        try:   
            text_file_name = str(input(color_text('Enter text file name (i.e. "filename"): ',Fore.CYAN)))
            if text_file_name.isalnum():
                pass
            else:
                print('That is an invalid filename. Please make sure not to include any invalid characters ( <>:"/\\|?* )')

            unique_file = f"{text_file_name}_{time.strftime('%Y_%m_%d_%H_%M')}.txt" 

            current_folder = os.getcwd()

            file_path_to_current_folder = os.path.join(current_folder, f"{unique_file}")

            with open(file_path_to_current_folder, 'w') as subnet_file:

                file_author_yn = str(input(color_text('Do you want to write a file author in your document? (y/n) ', Fore.YELLOW)).lower())
                while file_author_yn not in  ['y', 'n']:
                    print(color_text('That is not a valid input.', Fore.RED))
                    time.sleep(1.5)
                    file_author_yn = str(input(color_text('Do you want to add a file author in your document? (y/n) ', Fore.YELLOW)).lower())
                if file_author_yn == 'y':
                    file_author = (input(color_text('Enter file author: ', Fore.YELLOW)))
                    subnet_file.write(f'Network Name: {network_name}\nFile Author: {file_author}')
                    subnet_file.write('\n')
                elif file_author_yn == 'n':
                    pass

                subnet_count = int(input(color_text('How many subnets do you need? ', Fore.CYAN)))
                
                subnets = subnet_calculator(CIDR_network_ip_address, subnet_count)
                if len(subnets) < subnet_count:
                    print(color_text(f'Warning: Could not divide into exactly {subnet_count} subnets. Make sure to add your CIDR subnet mask at the end of your network address. (i.e. /24) In addition, make sure your subnet mask matches your network address. i.e. 1.0.0.0/8, 172.32.0.0/16, 192.168.10.0/24', Fore.RED))
                    return
            
                

                print(color_text(f'\nNetwork Name: {network_name}', Fore.GREEN))
                subnet_number = 0
                for subnet in subnets[:subnet_count]:
                    subnet_number += 1
                    print(color_text(f'\nSubnet {subnet_number}:', Fore.GREEN))
                    print(color_text(f'Network Address: {subnet.network_address}', Fore.MAGENTA))
                    print(color_text(f'Broadcast Address: {subnet.broadcast_address}', Fore.BLUE))
                    print(color_text(f'Range of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}', Fore.CYAN))

                    
                    subnet_file.write(f'\nSubnet {subnet_number}:')
                    subnet_file.write(f'\nNetwork Address: {subnet.network_address}')
                    subnet_file.write(f'\nBroadcast Address: {subnet.broadcast_address}')
                    subnet_file.write(f'\nRange of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}')
                    subnet_file.write('\n')
                print()
    
        except ValueError as val_err:
            print('ERROR: Make sure your network address and its subnet mask match with prefix of your address. Make sure you have a valid IP address.(i.e. 1.0.0.0/8, 172.32.0.0/16, 192.168.10.0/24)')

    #Prints subnet output to the terminal. Handles errors with an exception for incorrect user input.
    elif text_file_yn == 'n':
        
        try:
            subnet_number = 0

            subnet_count = int(input(color_text('How many subnets do you need? ', Fore.CYAN)))
                
            subnets = subnet_calculator(CIDR_network_ip_address, subnet_count)
            if len(subnets) < subnet_count:
                print(color_text(f'Warning: Could not divide into exactly {subnet_count} subnets. Make sure to add your CIDR subnet mask at the end of your network address. (i.e. /24) In addition, make sure your subnet mask matches your network address. (i.e. 1.0.0.0/8, 172.32.0.0/16, 192.168.10.0/24)', Fore.RED))
                return
            print(color_text(f'\nNetwork Name: {network_name}', Fore.GREEN))
            for subnet in subnets[:subnet_count]:
                subnet_number += 1
                print(color_text(f'\nSubnet {subnet_number}:', Fore.GREEN))
                print(color_text(f'Network Address: {subnet.network_address}', Fore.MAGENTA))
                print(color_text(f'Broadcast Address: {subnet.broadcast_address}', Fore.BLUE))
                print(color_text(f'Range of Usable IP addresses: {list(subnet.hosts())[0]} to {list(subnet.hosts())[-1]}', Fore.CYAN))
            print()

        except ValueError as val_err:
            print('ERROR: Make sure your network address and its subnet mask match with prefix of your address. Make sure you have a valid IP address.(i.e. 1.0.0.0/8, 172.32.0.0/16, 192.168.10.0/24)')

#Generates the subnet list based on the CIDR IP address and the desired number of subnets. Raises an error if the user's request surpasses the possible level of subnets.
def subnet_calculator(CIDR_network_ip_address, subnet_count):
    
    network = ipaddress.IPv4Network(f'{CIDR_network_ip_address}')

    network_portion_plus_subnet = network.prefixlen + (subnet_count - 1).bit_length()

    if network_portion_plus_subnet > 32:
        raise ValueError(f"Cannot divide {network} into {subnet_count} subnets. The required prefix length {network_portion_plus_subnet} is too large.")

    subnets = list(network.subnets(new_prefix=network_portion_plus_subnet))

    return subnets
    
#Makes color text which is fun
def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

#Centers text
def center_text(text):
    terminal_width = shutil.get_terminal_size().columns

    centered_text = text.center(terminal_width)
    
    return centered_text


if __name__ == "__main__":
    main()