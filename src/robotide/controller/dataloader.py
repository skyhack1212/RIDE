#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time
from threading import Thread

from robot.parsing.model import TestData


class DataLoader(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._namespace.reset_resource_and_library_cache()

    def load_datafile(self, path, load_observer):
        loader = _DataLoader(path)
        loader.start()
        load_observer.notify()
        while loader.isAlive():
            time.sleep(0.1)
            load_observer.notify()
        return loader.datafile

    def resources_for(self, datafile, load_observer):
        loader = _ResourceLoader(datafile, self._namespace.get_resources)
        loader.start()
        load_observer.notify()
        while loader.isAlive():
            time.sleep(0.1)
            load_observer.notify()
        return loader.resources


class _DataLoader(Thread):

    def __init__(self, path):
        Thread.__init__(self)
        self._path = path
        self.datafile = None

    def run(self):
        try:
            self.datafile = TestData(source=self._path)
        except Exception:
            pass
            # TODO: Log this error somehow


class _ResourceLoader(Thread):

    def __init__(self, datafile, resource_loader):
        Thread.__init__(self)
        self._datafile = datafile
        self._loader = resource_loader
        self.resources = []

    def run(self):
        self.resources = self._loader(self._datafile)
