#!/usr/bin/python3
import sys
import logging
import pam
from systemd.journal import JournaldLogHandler

PAM_SERVICE = "login"

##### BEGIN LOGGING SETUP #####
#Install dependencies
#apt install python3-dev python3-pip libsystemd-dev
#pip3 install systemd

# Get an instance of the logger object this module will use
logger = logging.getLogger(__name__)

# Instantiate the JournaldLogHandler to hook into systemd
journald_handler = JournaldLogHandler()

# Set a formatter to include the level name
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

# Add the journald handler to the current logger
logger.addHandler(journald_handler)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Log to stdout, DISABLE THIS IN PRODUCTION BY
#COMMENTING OUT THE NEXT LINE
handler.setFormatter(formatter)


#logger.addHandler(handler)

# Set the logging level
logger.setLevel(logging.DEBUG)

##### END OF LOGGING SETUP #####

logger.info(__name__)

#Input username:password
def main():
    username = None
    password = None
    result = False
    data = sys.stdin.read()
    
    logger.info("Received input: {0}".format(data))
    #Parse the username and password from the stdin input
    userpass=data.split(':')
    username=userpass[0]
    password=userpass[1]
    password=password.rstrip()
    print (f"{username} , {password}") #test to see if im grabbing the user and password right
    result=pam.authenticate(username, password, service="nginx_badidea") 
    print(f"Result: {result}") #print the result
    if (result):
     sys.stdout.write('True\n')
     return True
    else:
     sys.stdout.write('False\n')
     return False

    #Authenticate the username and password using
    #pam.authenticate()
    logger.info("Result: {0}".format(data))

    #Send the result of pam.authenticate to stdout

if __name__ == "__main__":
    main()
