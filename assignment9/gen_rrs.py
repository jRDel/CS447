#!/usr/bin/env python3
#Django ORM import
import os
import django
import sys
import argparse
import logging
import re
import ipaddress

#Configure the Django ORM
sys.path.insert(0,'/srv/apps/cs447')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cs447.settings'
django.setup()

from rdns import models

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='Dynamically Generate DNS Resource Records.')
parser.add_argument('--task', default='A', type=str,
                    help='What task to perform "A" or "PTR"')

parser.add_argument('--file', type=str,
                    help='Where should the output be saved?')

A_RR_FORMAT   = "{0}   IN      A         {1}"
PTR_RR_FORMAT = "{0}   IN      PTR       {1}"

def gen_a_rrs(hosts):
  output = []

  for h in hosts:
    #Create A record
    if h.hostname:
      #For some reason, h.hostname had a trailing newline with it so I had to replace it with ''
      hostname = h.hostname
      hostname = hostname.replace('\n','')
      string = (f"{hostname}   IN     A         {h.ip_address}")
      output.append(string)
    elif h.nmap_hostname:
      hostname = h.nmap_hostname
      hostname = hostname.replace('.ncr', '')
      string = (f"{hostname}   IN     A         {h.ip_address}")
      output.append(string)
    
  return output

def gen_ptr_rrs(hosts):
  output = []

  for h in hosts:
    #Create PTR record
    if h.hostname:
      #For some reason, h.hostname had a trailing newline with it so I had to replace it with ''
      hostname = h.hostname
      hostname = hostname.replace('\n','')
 #     ip_rev = reverse_ip(h.ip_address)
      ip= h.ip_address
      ip_end = ip.split(".")
      string = (f"{ip_end[3]}   IN     PTR         {hostname}")
      output.append(string)
    elif h.nmap_hostname:
      hostname = h.nmap_hostname
      hostname = hostname.replace('.ncr', '')
 #     ip_rev = reverse_ip(h.ip_address)
      ip= h.ip_address
      ip_end = ip.split(".")
      string = (f"{ip_end[3]}   IN     PTR         {hostname}")
      output.append(string)
    
  return output

#def reverse_ip(string): #Reversing the IP for PTR record
#  return ipaddress.ip_address(string).reverse_pointer

def main():
  args = parser.parse_args()
  hosts = models.Host.objects.all()
  rrs = []
  logger.info(f'Task: {args.task}')
  if args.task == 'A':
    logger.info('Generating A Records')
    rrs = gen_a_rrs(hosts)
  elif args.task == 'PTR':
    rrs = gen_ptr_rrs(hosts)
  else:
    logger.info('Invalid task, exiting.')
    sys.exit(1)

  if args.file:
    #Add newlines
    lines = [l + '\n' for l in rrs]
    f = open(args.file, 'w')
    f.writelines(lines)
    f.close()
    

if __name__ == '__main__':
  main()

