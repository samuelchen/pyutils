#!/usr/bin/env python
# coding: utf-8


import nmap
import datetime
import multiprocessing
import os
import sys
import simplejson as json
from queue import Empty
import socket
import logging

log = logging.getLogger(__name__)

DISCOVERED = 'discovered'
UNREACHABLE = 'error:unreachable'
UNRESOLVEABLE = 'error:dns_unresolveable'


def scan_host(host, queue, stop_event):
    nm = nmap.PortScanner()

    args = '-F -O --osscan-guess'
    scan_data = nm.scan(hosts=host, arguments=args)

    queue.put_nowait(scan_data)


class Scanner(object):
    queue = None
    nm = None

    def __init__(self, stop_event):
        self.nm = nmap.PortScanner()
        self.queue = multiprocessing.Queue()
        self.stop_event = stop_event
        self.process = multiprocessing.Process()

    def scan(self, hosts):

        # now accept only first
        # server_uuid = hosts[0]['server_uuid']
        # server_name = hosts[0]['server_name']

        # ip = self.resolve(server_name)
        # if not ip:
        #     # raise HostnameNotResolvedException('Hostname "%s" cannot be resolved.' % host)
        #     return {
        #         server_name: {
        #             "host": ip,
        #             "server_uuid": server_uuid,
        #             "status": UNRESOLVEABLE,
        #             "os": [],
        #             "ports": {}
        #         }
        #     }

        proc = multiprocessing.Process(target=scan_host, args=(hosts, self.queue, self.stop_event))

        log.info('Start to scan %s' % hosts)
        t = datetime.datetime.utcnow()

        proc.start()

        while proc.is_alive():
            if self.stop_event and self.stop_event.is_set():
                log.info('Stopping nmap process %d...' % proc.pid)
                proc.terminate()
                proc.join(3)
                if proc.is_alive():
                    log.warn('Nmap process %d is not stopped. Try killing...' % proc.pid)
                    # os.kill(proc.pid, 9)
                    os.system('kill -9 %d' % proc.pid)
                break
            proc.join(1)

        t = datetime.datetime.utcnow() - t
        log.info('time used: %s' % t)

        scan_data = {}
        try:
            scan_data = self.queue.get_nowait()
        except Empty:
            pass

        item = {
            "status": DISCOVERED,
            # "server_uuid": server_uuid,
            "host": '',
            "os": [],
            "ports": {}
        }

        items = []
        if 'scan' in scan_data:
            for host, data in scan_data['scan'].items():
                item['host'] = host

                if 'osmatch' in data:
                    for o in data['osmatch']:
                        item['os'].append({
                            "name": o['name'],
                            "accuracy": o['accuracy'],
                        })

                if 'portused' in data:
                    ports = item['ports']
                    for p in data['portused']:
                        ports[p['portid']] = {
                            "port": p['portid'],
                            "status": p['state'],
                            "protocol": p['proto']
                        }
                break  # now we have only one

            if len(item['os']) == 0 and len(item['ports']) == 0:
                item['status'] = UNREACHABLE

            items.append(item)

        return items

    def resolve(self, hostname):
        result = None
        try:
            result = socket.gethostbyname(hostname)
        except socket.gaierror as err:
            log.error('Can not resolve hostname "%s"' % hostname)

        return result

if __name__ == '__main__':
    sc = Scanner(None)
    result = sc.scan(sys.argv[1])
    with open('result.json', 'wt') as f:
        f.write(json.dumps(result))
