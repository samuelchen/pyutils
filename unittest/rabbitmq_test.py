#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
Test rabbitmq publisher and consumer

Created on 1/7/2015
'''

import unittest
from pyutils.rabbitmq import RabbitMQConsumer, RabbitMQPublisher
from pyutils.logger import Logger
import logging

logging.config.fileConfig('../logger.conf.sample')
from pyutils.logger import log



class RabbitMQTest(unittest.TestCase):

    def test_publisher(self):    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
        publisher = RabbitMQPublisher(host='localhost', port=35672, user='guest', password='guest', vhost='%2F?connection_attempts=3&heartbeat_interval=3600')
        #'amqp://guest:guest@localhost:35672/%2F?connection_attempts=3&heartbeat_interval=3600')
        try:
            publisher.run(exchange='pyutils', exchange_type='fanout', queue='pyutils.test', routing_key='#')
            for i in xrange(1000):
                publisher.send('message %d' % i)

        except KeyboardInterrupt:
            pass

        publisher.stop()
        self.assertEqual(True, False)

    def test_consumer(self):
        consumer = RabbitMQConsumer(host='localhost', port=35672, user='guest', password='guest', vhost='%2F')
        #'amqp://guest:guest@localhost:35672/%2F')
        try:
            consumer.run(exchange='pyutils', exchange_type='fanout', queue='pyutils.test', routing_key='#')
        except KeyboardInterrupt:
            consumer.stop()

        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
