#!/usr/bin/env python

import sys

from oslo.config import cfg
from oslo import messaging

from octavia.common import config
from octavia.openstack.common import log as logging

LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    config.init(sys.argv[1:])
    config.setup_logging(cfg.CONF)
    transport = messaging.get_transport(cfg.CONF)
    for key in cfg.CONF.keys():
        print("{0}={1}".format(key, getattr(cfg.CONF, key, None)))
        attr = getattr(cfg.CONF,key)
        if hasattr(attr,"items"):
            for (k,v) in attr.items():
                print("{0}.{1}={2}\n".format(key, k, v))
