#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""config
"""


import json
import os
import io


setting = {}
if os.path.isfile('./config.json'):
    with io.open('./config.json', encoding='utf-8') as f:
        settings = json.loads(f.read())
