#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""listener
"""
import ai
import alsaaudio
import config
import crystal
import collections
import time
from common import bytesframe
from crystals import pivot

_conf = config.settings.get('components', {}).get('listener', {})
_wakeup_words = _conf.get('wakeup-words', [])
_pcm = alsaaudio.PCM(
    type=alsaaudio.PCM_CAPTURE,
    mode=alsaaudio.PCM_NONBLOCK,
    device=_conf.get('device', 'default'),
)
_pcm.setchannels(_conf.get('channels', 1))
_pcm.setrate(_conf.get('rate', 16000))
_pcm.setformat(getattr(alsaaudio, _conf.get('format', 'PCM_FORMAT_S16_LE')))
_pcm.setperiodsize(_conf.get('periodsize', 160))
# 10 seconds
_capture_buffer = bytesframe.FixedBytesFrame(10)
_sound_bridge = collections.deque(maxlen=10)


class Recognizer(crystal.Crystal):
    """Recognizer
    """

    def __init__(self, *args, **kwargs):
        """__init__
        """
        super().__init__(*args, **kwargs)
        # wrap throttle
        self.identify = self.throttle(self.identify, wait=1)

    def recognize(self, frame):
        """recognize
        """
        _, res = ai.recognize(frame)
        print('recognize result:', res)
        if res in _wakeup_words:
            pivot.emit('angelia:wakeup')

    def identify(self, frame):
        """identify sound frame
        """
        self.call_soon_threadsafe(self.recognize, frame)

    def loop(self):
        """loop func
        """
        try:
            frame = _sound_bridge.popleft()
            self.identify(frame)
        except Exception:
            pass
        time.sleep(1)
        self.call_soon_threadsafe(self.loop)


class Listener(crystal.Crystal):
    """Listener
    """

    def loop(self):
        """loop func
        """
        while True:
            l, data = _pcm.read()
            if l:
                _capture_buffer.write(data)
                frame = _capture_buffer.subbuffer(3)
                _sound_bridge.append(frame)
            time.sleep(0.001)


listener = Listener(name='listener')
listener.daemon = True
recognizer = Recognizer(name='recognizer')
recognizer.daemon = True


def start():
    """start listener
    """
    listener.start()
    recognizer.start()


def stop():
    listener.stop()
    recognizer.stop()
