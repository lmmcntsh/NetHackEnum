#!/bin/python3
#UPDATED AUGUST 23
#import modules
import os
import sys
import argparse
import re
import subprocess


logo = """
    _   __     __               
   / | / ___  / /_              
  /  |/ / _ \/ __/              
 / /|  /  __/ /_                
/_/ |_/\___/\__/_           __  
          / / / ____ ______/ /__
         / /_/ / __ `/ ___/ //_/
        / __  / /_/ / /__/ ,<   
    ___/_/ /_/\__,_/\___/_/|_|  
   / ________  __  ______ ___   
  / __/ / __ \/ / / / __ `__ \  
 / /___/ / / / /_/ / / / / / /  
/_____/_/ /_/\__,_/_/ /_/ /_/   


"""

print(logo)

#Declare variables
tools = []
toolset = False
net_mode = False
target = " "
output_dir = " "


#checks if nmap is installed
def nmap_check():
    
    command = ['nmap', '--version']
    try:
        #Will run the command to check nmap's version (aka prove if its installed or not)
        subprocess.run(command, capture_output=True, text=True)
        
        print('[!] Nmap is installed. . . ')
        tools.append('1')

    except:
        tools.append('0')
        print('[!] Nmap is not installed')



#check_tools will check the system to ensure it has the necessary tools
def check_tools():
    print('[!] Checking for necessary tools. . . ')
    nmap_check()

    if '0' in tools:
        toolset = False
    else:
        toolset = True

    
    if toolset == False:
        print('[!] Please install necessary tools')
        exit()
    else:
        print('[+] Toolset installed')



#config will take the arguments and assign variables as needed before any actions are taken
def config():

    #Accessing necessary variables
    global net_mode
    global target
    global output_dir
    

    parser = argparse.ArgumentParser(description="NetHackEnum")

    parser.add_argument('net', nargs='?',
                        help= 'Sets tool to network mode, for scanning a network range rather than a single target')
    
    parser.add_argument('-t', metavar='--target', dest='target',
                        help= 'Sets the target for the script. Single IP address for single target mode, IP range for network mode')
    
    parser.add_argument('-o', nargs='?', metavar='--output', dest='output', 
                        help= 'Sets the name of the output directory. Default will be "NHE-<IP ADDRESS>"')
    

    #will take all the arguments for accessing
    args = parser.parse_args()

    #will check which mode to run the tool in (net or single mode)
    if args.net:
        net_mode = True
        print('[!] Network Mode')
    else:
        net_mode = False
        print('[!] Single Target Mode')

    if args.target:
        #Takes the target specified and ensures its a proper IP Address or range (based on net_mode or not)
        target = args.target
        if net_mode == True:
            pattern = r"^((\d{1,3}\.){3}\d{1,3})/(\d{1,2})$"
            if re.match(pattern, target):
                print('[!] Valid target')
            else:
                print('[!] INVALID TARGET')
                parser.print_help()
        else:
            pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$' #REGEX to see if the IP address is proper
            if re.match(pattern, target):
                print('[!] Valid target')
            else:
                print('[!] INVALID TARGET')
                parser.print_help()
    else:
        print('[!] NO TARGET SPECIFIED')
        parser.print_help()


    #Will set the output directory name to the one specified or the default NHE-IP
    if args.output:
        output_dir = args.output
    
    else:
        output_dir = "NHE-" + target


    # Give the user an option to overwrite or cancel
    while True:
        overwrite_choice = input(f"The directory '{output_dir}' already exists. Do you want to overwrite it? (y/n): ")
        if overwrite_choice.lower() == 'y':
            os.system('rm -r {}'.format(output_dir))  # Remove existing directory
            os.system('mkdir {}'.format(output_dir))  # Recreate directory if user chooses to overwrite
            break
        elif overwrite_choice.lower() == 'n':
            print("Operation canceled. Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please enter 'y' to overwrite or 'n' to cancel.")
        
    # Check if the directory exists
    if os.path.isdir(output_dir):
        print(f"Directory '{output_dir}' successfully created.")
    else:
        print(f"Failed to create directory '{output_dir}'.")
        sys.exit()
    
    

#will simply scan one target for open ports
def single_nmap_simple_scan():

    print('\n-----NMAP PORT SCAN-----\n')
    print('[+] Beginning simple Nmap scan. . . ')
    #output = subprocess.run('echo nmap {} -p- -nO {}/simple_nmap_scan'.format(target,output_dir), capture_output=True, text=True)
    os.system('nmap {} -p- -oN {}/simple_nmap_scan.txt > /dev/null 2>&1'.format(target, output_dir))

    print('[+] Nmap scan results stored in {} directory'.format(output_dir))
    

#Will read nmap output file and return which ports were found open on the machine
def nmap_open_ports():
    print('[+] Peeping open ports. . .')
    #NOTE CHANGE THE FILE TO THE VARIABLE AFTER THE TEST
    with open('{}/simple_nmap_scan.txt'.format(output_dir)) as file:
        output = file.read()
    global open_ports
    open_ports =  re.findall(r"\b(\d+)\/(?:tcp|udp)\s+open\b", output)
    
    file.close()



#Will read the deeper nmap output file and return the ports and their version information
def nmap_port_info():
    print('\n-----PORT INFORMATION: {} -----\n'.format(target))
    print('PORT     SERVICE     VERSION')
    port_lines = []
    with open('{}/simple_nmap_scan') as f:
        
        file = f.readlines()
    
        #takes every line from the file and if it has an open port it will be saved to port_lines
        for line in file:
            for port in open_ports:
                if port in line:
                    port_lines.append(line.rstrip('\n'))
                    break
        
        
        #will print out the port and the corresponding info
        port_info = []
        for line, port in zip(port_lines, open_ports):
            words = line.split()
            words.remove(words[0])
            words.remove('open')
            result = ' '.join(words)
            port_info.append(result)
        for port, info in zip(open_ports, port_info):
                print('{:<8}    {}'.format(port, info))
        
        f.close()
        





def deep_nmap_scan():
    print('\n-----DEEP VERSION SCAN-----\n')
    print('[+] Diving deeper on open ports. . . ')
    open_ports_str = ','.join(map(str, open_ports))
    os.system('nmap -p {} -sV {} -oN {}/deep_nmap_scan.txt > /dev/null 2>&1'.format(open_ports_str, target, output_dir))
    print('[+] Nmap scan results stored in {} directory'.format(output_dir))


#Will scan network for live hosts
def net_host_scan():
    print('\n-----NMAP LIVE HOST SCAN-----\n')
    print('[+] Scanning for live hosts. . . ')
    os.system('nmap -sn {} -oN {}/live_hosts'.format(target))
    print('[+] Live hosts stored in {} directory'.format(output_dir))


#Will check to see if port 80 or 443 is open, and will attempt basic directory enumeration
def directory_enum():
    print('\n-----DIRECTORY ENUMERATION-----\n')
    if "80" or "443" in open_ports:
        print('[+] Webserver found. . . ')




    else:
        print('[!] No Webserver found on target (Both port 80 and 443 are not open)')





#### DISPLAY FUNCTIONS ####
#Sole purpose is for displaying the information found, but pretty lmao
        
def list_open_ports():
    print('--> OPEN PORTS <--')
    for port in open_ports:
        print(f'{port}')


def list_service_info():
    # Define the start and end markers for the section to extract
    start_marker = "Host is up"
    end_marker = "Service detection performed"

    # Flag to indicate whether to print lines within the desired section
    printing = False

    # Read the file and print the desired section
    with open('your_file_path.txt', 'r') as file:
        for line in file:
            # Check if the start marker is found in the line
            if start_marker in line:
                printing = True
            # Check if the end marker is found in the line
            elif end_marker in line:
                break  # Stop printing when the end marker is found
            # Print the line if the printing flag is True
            if printing:
                print(line.strip())

#CLUSTER FUNCTIONS
#These functions combine smaller functions from above to make them easier to run (all nmap functions working in tandem for example)

def single_target_nmap_full():
    #will do the basic nmap scan
    single_nmap_simple_scan()

    #takes the basic scan and retrieves the open ports only
    nmap_open_ports()

    list_open_ports()

    #will take only the open ports and run a deeper scan on them
    deep_nmap_scan()
    
    #show the service information
    list_service_info()










if __name__ == '__main__':
    check_tools()
    config()

    #script path for single target mode
    if net_mode == True:
        net_host_scan()


    elif net_mode == False:
        try:
            single_target_nmap_full()
            
            
        except KeyboardInterrupt:
            print('-----KEYBOARD INTERRUPT-----')
