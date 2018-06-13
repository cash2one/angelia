#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""listener
"""
from common import events

pivot = events.EventEmitter()

def emit(*args, **kwargs):
    """alisa for pivot.emit
    """
    return pivot.emit(*args, **kwargs)


def on(*args, **kwargs):
    """alias for pivot.on
    """
    return pivot.on(*args, **kwargs)


def off(*args, **kwargs):
    """alias for pivot.off
    """
    return pivot.off(*args, **kwargs)
