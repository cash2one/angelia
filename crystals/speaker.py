#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""speaker
"""
import ai
import time
import alsaaudio
import subprocess
import config
import crystal
from crystals import pivot


_conf = config.settings.get('components', {}).get('speaker', {})
_pcm = alsaaudio.PCM(
    type=alsaaudio.PCM_PLAYBACK,
    mode=alsaaudio.PCM_NONBLOCK,
    device=_conf.get('device', 'default'),
)
_pcm.setchannels(_conf.get('channels', 1))
_pcm.setrate(_conf.get('rate', 16000))
_pcm.setformat(getattr(alsaaudio, _conf.get('format', 'PCM_FORMAT_S16_LE')))
_pcm.setperiodsize(_conf.get('periodsize', 160))


def mpeg2pcm(src):
    """convert mpeg to pcm
    """
    proc = subprocess.Popen(
        ['ffmpeg', '-i', 'pipe:0', '-f', 's16le', 'pipe:1'],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    sout, serr = proc.communicate(input=src)
    return sout


def play(clip):
    """play
    """
    idx = 0
    length = len(clip)
    while idx < length:
        writed = _pcm.write(clip[idx:idx+2])
        if writed > 0:
            idx += 2


class Speaker(crystal.Crystal):
    """Speaker
    """

    def speak(self, *args, **kwargs):
        """speak
        """
        clip = ai.synthesize(u'你好，什么事')
        if clip is not None:
            play(mpeg2pcm(clip))

    def loop(self):
        """loop func
        """
        pivot.on('angelia:wakeup', self.speak)
        while True:
            time.sleep(1)


speaker = Speaker(name='speaker')
speaker.daemon = True


def start():
    """Start speaker
    """
    speaker.start()


def stop():
    """Stop speaker
    """
    speaker.stop()
