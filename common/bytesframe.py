#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bytes frame
"""
import alsaaudio
from common import utils
from common import events


def bytes2int_ule(bs):
    """convert bytes to little endian unsigned integer
    """
    return int.from_bytes(bs, byteorder='little', signed=False)


def bytes2int_sle(bs):
    """convert bytes to little endian signed integer
    """
    return int.from_bytes(bs, byteorder='little', signed=True)


def bytes2int_ube(bs):
    """convert bytes to big endian unsigned integer
    """
    return int.from_bytes(bs, byteorder='big', signed=False)


def bytes2int_sbe(bs):
    """convert bytes to big endian signed integer
    """
    return int.from_bytes(bs, byteorder='big', signed=True)


_pcm_format_transformer_map = {
    alsaaudio.PCM_FORMAT_S8: bytes2int_ule,
    alsaaudio.PCM_FORMAT_U8: bytes2int_sle,
    alsaaudio.PCM_FORMAT_S16_LE: bytes2int_sle,
    alsaaudio.PCM_FORMAT_S16_BE: bytes2int_sbe,
    alsaaudio.PCM_FORMAT_U16_LE: bytes2int_ule,
    alsaaudio.PCM_FORMAT_U16_BE: bytes2int_ube,
    alsaaudio.PCM_FORMAT_S24_LE: bytes2int_sle,
    alsaaudio.PCM_FORMAT_S24_BE: bytes2int_sbe,
    alsaaudio.PCM_FORMAT_U24_LE: bytes2int_ule,
    alsaaudio.PCM_FORMAT_U24_BE: bytes2int_ube,
    alsaaudio.PCM_FORMAT_S32_LE: bytes2int_sle,
    alsaaudio.PCM_FORMAT_S32_BE: bytes2int_sbe,
    alsaaudio.PCM_FORMAT_U32_LE: bytes2int_ule,
    alsaaudio.PCM_FORMAT_U32_BE: bytes2int_ube,
    # alsaaudio.PCM_FORMAT_FLOAT_LE
    # alsaaudio.PCM_FORMAT_FLOAT_BE
    # alsaaudio.PCM_FORMAT_FLOAT64_LE
    # alsaaudio.PCM_FORMAT_FLOAT64_BE
    # alsaaudio.PCM_FORMAT_MU_LAW
    # alsaaudio.PCM_FORMAT_A_LAW
    # alsaaudio.PCM_FORMAT_IMA_ADPCM
    # alsaaudio.PCM_FORMAT_MPEG
    # alsaaudio.PCM_FORMAT_GSM
    # alsaaudio.PCM_FORMAT_S24_3LE
    # alsaaudio.PCM_FORMAT_S24_3BE
    # alsaaudio.PCM_FORMAT_U24_3LE
    # alsaaudio.PCM_FORMAT_U24_3BE
    # alsaaudio.PCM_FORMAT_DSD_U8
    # alsaaudio.PCM_FORMAT_DSD_U16_LE
    # alsaaudio.PCM_FORMAT_DSD_U32_LE
    # alsaaudio.PCM_FORMAT_DSD_U32_BE
}


_pcm_format_bits_map = {
    alsaaudio.PCM_FORMAT_S8: 8,
    alsaaudio.PCM_FORMAT_U8: 8,
    alsaaudio.PCM_FORMAT_S16_LE: 16,
    alsaaudio.PCM_FORMAT_S16_BE: 16,
    alsaaudio.PCM_FORMAT_U16_LE: 16,
    alsaaudio.PCM_FORMAT_U16_BE: 16,
    alsaaudio.PCM_FORMAT_S24_LE: 24,
    alsaaudio.PCM_FORMAT_S24_BE: 24,
    alsaaudio.PCM_FORMAT_U24_LE: 24,
    alsaaudio.PCM_FORMAT_U24_BE: 24,
    alsaaudio.PCM_FORMAT_S32_LE: 32,
    alsaaudio.PCM_FORMAT_S32_BE: 32,
    alsaaudio.PCM_FORMAT_U32_LE: 32,
    alsaaudio.PCM_FORMAT_U32_BE: 32,
    # alsaaudio.PCM_FORMAT_FLOAT_LE
    # alsaaudio.PCM_FORMAT_FLOAT_BE
    # alsaaudio.PCM_FORMAT_FLOAT64_LE
    # alsaaudio.PCM_FORMAT_FLOAT64_BE
    # alsaaudio.PCM_FORMAT_MU_LAW
    # alsaaudio.PCM_FORMAT_A_LAW
    # alsaaudio.PCM_FORMAT_IMA_ADPCM
    # alsaaudio.PCM_FORMAT_MPEG
    # alsaaudio.PCM_FORMAT_GSM
    # alsaaudio.PCM_FORMAT_S24_3LE
    # alsaaudio.PCM_FORMAT_S24_3BE
    # alsaaudio.PCM_FORMAT_U24_3LE
    # alsaaudio.PCM_FORMAT_U24_3BE
    # alsaaudio.PCM_FORMAT_DSD_U8
    # alsaaudio.PCM_FORMAT_DSD_U16_LE
    # alsaaudio.PCM_FORMAT_DSD_U32_LE
    # alsaaudio.PCM_FORMAT_DSD_U32_BE
}


@utils.memorize
def get_framesize(elapse,
                  rate=16000, format=alsaaudio.PCM_FORMAT_S16_LE, channels=1):
    """calculate size of frame in `bytes`
    """
    return rate * _pcm_format_bits_map.get(format) * elapse * channels // 8


class FixedBytesFrame(events.EventEmitter):
    """bytes frame with fixed size
    """
    def __init__(self, elapse=3,
                 rate=16000, format=alsaaudio.PCM_FORMAT_S16_LE, channels=1):
        """__init__
        """
        super().__init__()
        self.__buffer__ = bytes()
        self.__elapse__ = elapse
        self.__rate__ = rate
        self.__format__ = format
        self.__channels__ = channels

    def size(self):
        """get frame size
        """
        return get_framesize(
            self.__elapse__,
            rate=self.__rate__,
            format=self.__format__,
            channels=self.__channels__,
        )

    def buffer(self):
        """get buffer
        """
        return self.__buffer__

    def write(self, buf):
        """write
        """
        size = len(buf)
        if size > 0:
            self.__buffer__ = self.__buffer__[0 - self.size() + size:] + buf
            self.emit('change', size=size)

    def subbuffer(self, elapse):
        """cut frame
        """
        size = get_framesize(
            elapse,
            rate=self.__rate__,
            format=self.__format__,
            channels=self.__channels__,
        )
        return self.buffer()[0 - size:]
