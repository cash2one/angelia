#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""crystal
"""
import threading
import asyncio
from common import utils
from common import events


class Crystal(threading.Thread, events.EventEmitter):
    """Crystal
    """
    def __init__(self, *args, **kwargs):
        """__init__
        """
        threading.Thread.__init__(self, *args, **kwargs)
        events.EventEmitter.__init__(self, *args, **kwargs)
        self.__event_loop__ = asyncio.new_event_loop()

    def throttle(self, func, wait=1):
        """bind event loop to utils.throttle
        """
        return utils.throttle(func, wait, loop=self.__event_loop__)

    def call_soon_threadsafe(self, func, *args, **kwargs):
        """call func soon on event loop
        """
        return self.__event_loop__.call_soon_threadsafe(func, *args, **kwargs)

    def call_later(self, func, *args, **kwargs):
        """call later on event loop
        """
        return self.__event_loop__.call_later(func, *args, **kwargs)

    def run_forever(self):
        """run event loop forever
        """
        self.__event_loop__.run_forever()

    def loop(self):
        """loop func
        it invoke `target` function default which passed to `__init__`
        """
        target = self._target
        print('run loop', target)
        if target is None:
            target = utils.noop
        return target(*self._args, **self._kwargs)

    def run(self):
        """run
        """
        self.call_soon_threadsafe(self.loop)
        print('event loop on %s' % (self.name))
        self.run_forever()

    def stop(self):
        """stop crystal thread
        """
        self.__event_loop__.stop()
