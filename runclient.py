#!/usr/bin/env python
"""
This is a trivial example of how to use kismetclient in an application.
"""
from kismetclient import Client as KismetClient
from kismetclient import handlers
import httplib2
from pprint import pprint

import logging
log = logging.getLogger('kismetclient')
log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


address = ('127.0.0.1', 2501)
k = KismetClient(address)
#k.register_handler('TRACKINFO', handlers.print_fields)


def handle_ssid(client, ssid, mac, type):
    type_human = "unknown"
    if type == "0":
        type_human = 'ap'
    if type == "2":
        type_human = 'ap_probe'
    send_data('network/' + ssid + '/' + mac + '/' + type_human )

def handle_client(client, bssid, mac):
    send_data('client/' + mac + '/' + bssid)

def send_data(url):
    full_url = "http://www.hecko.net/" + url
    print "sending to url " + full_url
    resp, content = httplib2.Http().request(full_url)

k.register_handler('SSID', handle_ssid)
k.register_handler('CLIENT', handle_client)

try:
    while True:
        k.listen()
except KeyboardInterrupt:
    pprint(k.protocols)
    log.info('Exiting...')
