# -*- coding: utf-8 -*-
"""

    Copyright (C) 2018-2018 plugin.video.youtube

    SPDX-License-Identifier: GPL-2.0-only
    See LICENSES/GPL-2.0-only for more information.
"""

import json
import os

import xbmcaddon
import xbmcvfs

from ..logger import log_debug, log_error
from ..utils import make_dirs


class JSONStore(object):
    def __init__(self, filename):
        addon_id = 'plugin.video.youtube'
        addon = xbmcaddon.Addon(addon_id)

        self.base_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

        if not xbmcvfs.exists(self.base_path) and not make_dirs(self.base_path):
            log_error('JSONStore.__init__ |{path}| invalid path'.format(
                path=self.base_path
            ))
            return

        self.filename = os.path.join(self.base_path, filename)
        self._data = {}
        self.load()
        self.set_defaults()

    def set_defaults(self, reset=False):
        raise NotImplementedError

    def save(self, data):
        if data == self._data:
            log_debug('JSONStore.save |{filename}| data unchanged'.format(
                    filename=self.filename
            ))
            return
        log_debug('JSONStore.save |{filename}|'.format(
            filename=self.filename
        ))
        try:
            if not data:
                raise ValueError
            _data = json.loads(json.dumps(data))
            with open(self.filename, mode='w', encoding='utf-8') as jsonfile:
                json.dump(_data, jsonfile, indent=4, sort_keys=True)
            self._data = _data
        except (IOError, OSError):
            log_error('JSONStore.save |{filename}| no access to file'.format(
                filename=self.filename
            ))
            return
        except (TypeError, ValueError):
            log_error('JSONStore.save |{data}| invalid data'.format(
                data=data
            ))
            self.set_defaults(reset=True)

    def load(self):
        log_debug('JSONStore.load |{filename}|'.format(
            filename=self.filename
        ))
        try:
            with open(self.filename, mode='r', encoding='utf-8') as jsonfile:
                data = jsonfile.read()
            if not data:
                raise ValueError
            self._data = json.loads(data)
        except (IOError, OSError):
            log_error('JSONStore.load |{filename}| no access to file'.format(
                filename=self.filename
            ))
        except (TypeError, ValueError):
            log_error('JSONStore.load |{data}| invalid data'.format(
                data=data
            ))

    def get_data(self):
        try:
            if not self._data:
                raise ValueError
            return json.loads(json.dumps(self._data))
        except (TypeError, ValueError):
            log_error('JSONStore.get_data |{data}| invalid data'.format(
                data=self._data
            ))
            self.set_defaults(reset=True)
        return json.loads(json.dumps(self._data))
