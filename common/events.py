#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""events
"""
import asyncio


class Event(object):
    """Event
    """
    def __init__(self, event_type, target, *args, **kwargs):
        """__init__
        """
        super().__init__()
        self.__type__ = event_type
        self.__target__ = target
        self.args = args
        self.kwargs = kwargs

    def type(self):
        """Get event type
        """
        return self.__type__

    def target(self):
        """Get event target
        """
        return self.__target__


class EventEmitter(object):
    """EventEmitter
    """
    def __init__(self, loop=None, *args, **kwargs):
        """__init__
        """
        super().__init__()
        if loop is None:
            loop = asyncio.get_event_loop()
        self.__event_loop__ = loop
        self.__handler_pool__ = {}

    def on(self, evt_name, handler):
        """add event listener
        """
        handlers = self.__handler_pool__.get(evt_name, ())
        handlers += (handler,)
        self.__handler_pool__[evt_name] = handlers

    def off(self, evt_name, handler=None):
        """remove event listener
        """
        handlers = self.__handler_pool__.get(evt_name, ())
        if handler is None:
            handlers = ()
        handlers = tuple(filter(lambda x: x is not handler, handlers))
        self.__handler_pool__[evt_name] = handlers

    def emit(self, evt_name, *args, **kwargs):
        """emit event
        """
        evt = Event(evt_name, self, *args, **kwargs)
        handlers = self.__handler_pool__.get(evt_name, ())
        for handler in handlers:
            self.__event_loop__.call_soon_threadsafe(handler, evt)
