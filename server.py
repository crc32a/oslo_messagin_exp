#!/usr/bin/env python

import os
import sys
import logging
import datetime
import time
import eventlet
eventlet.monkey_patch()
server = "server"
topic = "my_topic"

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
fp = open(os.path.expanduser("~/log.txt"),"a")

target = messaging.Target(topic=topic,version="5.0",
                          server=server)


class EndPoint(object):
    def __init__(self):
        self.target = target
        self.throw_exception = False
    def toggle_exception(self,ctx,**kw):
        self.throw_exception = not self.throw_exception
    def some_method(self,ctx,**kw):
        if self.throw_exception:
            raise ValueError("Some Exception")
        for (k,v) in ctx.iteritems():
            print "ctx[%s] = %s\n"%(k,v)
        for (k,v) in kw.iteritems():
            print "kw[%s] = %s"%(k,v)
        time.sleep(1.0)
        fmt = "%s msg_id=%i pid=%i"
        fp.write(fmt%(datetime.datetime.now(),kw["mid"],os.getpid()))
        fp.write("\n")
        fp.flush()

ep = EndPoint()
server = messaging.get_rpc_server(transport,
                                  target,
                                  [ep],
                                  executor="eventlet")
server.start()

while True:
    time.sleep(0.25)

