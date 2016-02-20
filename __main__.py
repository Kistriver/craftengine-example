# -*- coding: utf-8 -*-
__author__ = "Alexey Kachalov"

import os
import time
import logging
import signal
import threading

from pycraftengine.exceptions import KernelException
from pycraftengine.rpc import Rpc

logging.basicConfig(format="[%(threadName)s][%(asctime)-15s] %(message)s")
logger = logging.getLogger("craftengine")
logger.setLevel("DEBUG")

rpc = None


def main():
    global rpc
    signal.signal(signal.SIGTERM, exit)
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGPWR, exit)

    service, instance, address, token = \
        os.environ.get("CE_NAME", ""), \
        int(os.environ.get("CE_INSTANCE", 1)), \
        ("ce-kernel", 2011), \
        os.environ.get("CE_TOKEN", "")

    rpc = Rpc(service, instance, address, token, threads=1, params={})
    threading.Thread(target=rpc.serve).start()

    rpc.bind("test", lambda *args, **kwargs: print(args, kwargs))

    self = rpc("test", "alpha")

    time.sleep(6)
    while True:
        try:
            self.sync().test(service, instance, token)
        except KernelException:
            pass
        time.sleep(10)

    while rpc.alive:
        time.sleep(1)


def exit(*args, **kwargs):
    global rpc
    logger.debug("Stopping...")
    rpc.close()

if __name__ == "__main__":
    try:
        main()
    except:
        rpc.close()
