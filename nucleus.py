#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nucleus
"""
import asyncio
from crystals import listener
from crystals import speaker


def main():
    """Main entry
    """
    loop = asyncio.get_event_loop()
    try:
        print('start')
        listener.start()
        print('listener started')
        speaker.start()
        print('speaker started')
        print('event loop on main')
        loop.run_forever()
    except KeyboardInterrupt:
        listener.stop()
        speaker.stop()
        loop.stop()


if __name__ == '__main__':
    main()
