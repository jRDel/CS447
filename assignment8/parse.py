#!/usr/bin/env python3
import xml.etree.ElementTree as ET
#Django ORM import
import os
import django
import sys
import requests
import subprocess
from datetime import datetime, timedelta

#Configure the Django ORM
sys.path.insert(0,'/srv/apps/cs447')
os.environ["DJANGO_SETTINGS_MODULE"] = 'cs447.settings'
django.setup()

#Use models.Host to create database records
from rdns import models
from rdns import views

tree = ET.parse('output.xml')

root = tree.getroot()

hosts = root.findall("./host") #list of nodes that are host field

#example time using date command: Mon 12 Apr 2021 04:00:52 AM UTC
start = root.attrib.get('startstr', None) #gives something like "Mon Apr 12 02:32:52 2021"
datetime_obj = datetime.strptime(start, '%a %b %d %H:%M:%S %Y')

def gethostname(ip_address):
  hostname = ''
  url = f'http://{ip_address}/rdns/hostname'
  response=requests.get(url, timeout=1)
  print(response.status_code)
  if response.status_code == 200:
    hostname = response.text[:32]
  return hostname

for child in hosts: #parsing nodes in this list of host, children

  mac = None
  reportedhostname = None
  nmap_hostname = None
  ip = None
  updown = None
  online = False
  addresses = child.findall("./address")
  hostnames = child.findall("./hostnames/hostname")
  status = child.find("./status")
  
  #Get the hostname of the child
  for h in hostnames:
    htype = h.attrib.get('type', None)
    if htype: #if htype not None, then it has a hostname, otherwise pass
     nmap_hostname = h.attrib.get('name', None)
    else:
     pass

  #Get the status of the child
  for s in status:
    updown = s.attrib.get('state', None)
    if updown == 'up':
     online=True
    else:
     online=False

  #Print out addresses
  for a in addresses:
    atype = a.attrib.get('addrtype', None)
    if atype is not None:
     if atype == 'mac':
      mac = a.attrib.get('addr', None)
     if atype == 'ipv4':
      ip = a.attrib.get('addr', None)
  http = child.find(".//*[@portid = '80']")
  state = http.find("./state")
  if state.attrib['state'] == 'open':   
    reportedhostname=gethostname(ip)
  #add host to database with associated values
  
  host = models.Host.objects.filter(mac_address=mac).first()
  if mac is not None and host is None: #Record has never existed before
    host = models.Host()
    host.mac_address = mac
    host.hostname = reportedhostname
    host.nmap_hostname = nmap_hostname
    host.ip_address = ip
    host.online = online
    host.last_update = datetime_obj
    host.save()
  
  elif mac is not None:
    host.mac_address = mac
    host.hostname = reportedhostname
    host.nmap_hostname = nmap_hostname
    host.ip_address = ip
    host.online = online
    host.last_update = datetime_obj
    host.save()
  else:
    pass
    
  #print(f"MAC: {mac}")
  #print(f"Associated Hostname: {hostname}")
  #host = models.Host.objects.filter(mac_address=mac).first()
  
