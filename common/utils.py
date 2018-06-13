#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""utils
"""
import asyncio
import time
import functools


def noop(*args, **kwargs):
    """no-op
    """
    pass


def memorize(func):
    """cache result of func by arguments hash
    """
    cache = {}

    def wrapper(*args, **kwargs):
        """memorize wrapper
        """
        key = hash((args, tuple(kwargs.items())))
        if key in cache:
            return cache.get(key)
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper


def asynchronize(func):
    """Make func to be asynchronous
    """
    async def async_wrapper(*args, **kwargs):
        """async wrapper
        """
        return await asyncio.coroutine(func)(*args, **kwargs)
    return async_wrapper


def throttle(func, wait=1, loop=None):
    """throttle wrapper
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    last = 0
    timer = None

    def delay(*args, **kwargs):
        """throttle delay wrapper
        """
        nonlocal last
        nonlocal timer
        last = time.time()
        timer = None
        func(*args, **kwargs)

    def wrapper(*args, **kwargs):
        """throttle wrapper
        """
        nonlocal last
        nonlocal timer
        now = time.time()
        remain = wait - (now - last)
        if remain <= 0 or remain > wait:
            if timer is not None:
                timer.cancel()
                timer = None
            last = now
            func(*args, **kwargs)
        else:
            if timer is not None:
                timer.cancel()
            timer = loop.call_later(
                remain,
                functools.partial(delay, *args, **kwargs)
            )

    return wrapper
