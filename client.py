#!/usr/bin/env python

import sys
import logging

from oslo.config import cfg
from oslo import messaging


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
ch.setFormatter(formatter)
root.addHandler(ch)



cfg.CONF(project="octavia")

transport = messaging.get_transport(cfg.CONF)

target = messaging.Target(topic="my_topic",version="5.0",fanout=False)
client = messaging.RPCClient(transport, target=target)

mid = 0
def cast(*args):
    global mid
    n=1
    topic = None
    server = None
    if len(args)>=1:
        n = args[0]
    if len(args)>=2:
        ctx = client.prepare(topic=args[1])
    if len(args)>=3:
        ctx = ctx.prepare(server=args[2])
    for i in xrange(0,n):
        ctx.cast({},"some_method",test="test",up="yours",mid=mid)
        mid += 1

def toggle_exc():
    client.cast({},"toggle_exception",**{})

