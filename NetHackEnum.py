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


#config will take the arguments and assign variables as needed before any actions are taken
def config():
    parser = argparse.ArgumentParser(description="NetHackEnum")
    parser.add_argument('--net', help= 'test')


    args = parser.parse_args()

    if args.net:
        net_mode = True
        print('[!] Network Mode')
    else:
         print('[!] Single Target Mode')  


config()
