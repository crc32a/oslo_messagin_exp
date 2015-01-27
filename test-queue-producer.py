import sys
import uuid

from oslo.config import cfg
from oslo import messaging

from octavia.common import config

#Must be run before producer is imported
config.init(sys.argv[1:])
config.setup_logging(cfg.CONF)


from octavia.api.v1.handlers.queue import producer

if __name__ == "__main__":

    prod_handler = producer.ProducerHandler()
    print cfg.CONF.oslo_messaging.exchange
    print cfg.CONF.oslo_messaging.topic
    i=0
    for handler in [prod_handler.load_balancer, prod_handler.listener,
                    prod_handler.pool, prod_handler.health_monitor,
                    prod_handler.member]:
        i += 1
        update_dict = {"test": "some", "values":":)"}
        handler.create({}, i)
        handler.update({}, update_dict, i)
        handler.delete({},  i)


