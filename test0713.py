# -*- coding:utf-8 -*-
import threading
import os
from time import ctime,sleep
import requests
import json

import ctypes
dll = ctypes.WinDLL('test.dll')
