#!/usr/bin/env python

from oslo.config import cfg
from oslo import messaging

cfg.CONF(project="octavia")

transport = messaging.get_transport(cfg.CONF)
for key in transport.conf.keys():
    print "%s=%s"%(key,getattr(transport.conf,key,None))
