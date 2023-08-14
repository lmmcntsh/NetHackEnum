#import modules
import os
import sys
import argparse


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

#process variables
net_mode = False
target = " "

#config will take the arguments and assign variables as needed before any actions are taken
def config():

    global net_mode
    global target

    parser = argparse.ArgumentParser(description="NetHackEnum")

    parser.add_argument('net', nargs='?',
                        help= 'Sets tool to network mode, for scanning a network range rather than a single target')
    
    parser.add_argument('-t', metavar='--target', dest='target')

    #will take all the arguments for accessing
    args = parser.parse_args()

    if args.net:
        net_mode = True
        print('[!] Network Mode')
    else:
         net_mode = False
         print('[!] Single Target Mode')

    if 

    target = args.target


config()
print(target)