#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ai interface wrap
"""
import aip
import config


_conf = config.settings.get('components', {}).get('baidu-aip')
_token = map(
    lambda x: _conf.get(x, ''),
    [
        'app-id',
        'app-key',
        'secret-key',
    ]
)
_speech_client = aip.AipSpeech(*_token)
_speech_client.setConnectionTimeoutInMillis(3000)
_speech_client.setSocketTimeoutInMillis(3000)

_default_recognize_opts = {
    'dev_pid': 1536,
}

_default_synthesize_opts = {
    'spd': 5,
    'pit': 5,
    'vol': 5,
    'per': 3,
}


def recognize(speech, **kwargs):
    """recognize
    """
    format = 'pcm'
    rate = 16000
    opts = {**_default_recognize_opts, **kwargs}
    result = _speech_client.asr(speech, format, rate, opts)
    code = result.get('err_no')
    if code != 0:
        return code, None
    return code, result.get('result')[0]


def synthesize(text, **kwargs):
    """synthesize
    """
    ctp = 1
    lang = 'zh'
    opts = {**_default_synthesize_opts, **kwargs}
    result = _speech_client.synthesis(text, lang, ctp, opts)
    if not isinstance(result, dict):
        return result
    return None
