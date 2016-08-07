#!/usr/bin/python

import os
from ConfigParser import ConfigParser

class MySQLConfig(ConfigParser):
    def __init__(self, config, **kw):
        ConfigParser.__init__(self, allow_no_value=True)
        
    def     
