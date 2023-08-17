#!/bin/python3
#UPDATED AUGUST 16
#import modules
import os
import sys
import argparse
import re


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
net_mode = False
target = " "
output_dir = " "



#check_tools will check the system to ensure it has the necessary tools
def check_tools():
    print("hi")

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
            pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
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

    os.system('mkdir {}'.format(output_dir))


    os.system('cd {}'.format(output_dir))

    

#will simply scan one target for open ports
def single_nmap_simple_scan():

    print('\n-----NMAP SCAN-----\n')
    print('[+] Beginning simple Nmap scan. . . ')
    os.system('echo nmap {} -p- -nO {}/simple_nmap_scan'.format(target,output_dir))
    print('[+] Nmap scan results stored in {} directory'.format(output_dir))

#Will scan network for live hosts
def net_host_scan():
    print('\n-----NMAP LIVE HOST SCAN-----\n')
    print('[+] Scanning for live hosts. . . ')
    os.system('echo nmap -sn {} -nO {}/live_hosts'.format(target))
    print('[+] Live hosts stored in {} directory'.format(output_dir))






    



config()
print(target)
print(output_dir)
single_nmap_simple_scan()