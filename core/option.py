#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import ConfigParser 

from thirdparty.attrdict import AttrDict
from core.data import paths
from comm.utils import getUnicode, checkFile


def initOptions(inputOptions=AttrDict(), overrideOptions=False):
    _mergeOptions(inputOptions, overrideOptions)


def _mergeOptions(inputOptions, overrideOptions):
    configFile = paths.CONFIG_FILE_PATH
    checkFile(configFile)
    try:
        config=ConfigParser.ConfigParser()
        config.read(configFile)
    except Exception, ex:
        errMsg = "you have provided an invalid and/or unreadable configuration file ('%s')" % getUnicode(ex)
        raise Exception(errMsg)

    for section in config.sections():
        for option in config.options(section):
            mergeOption = config.get(section, option)
            if mergeOption and _isDefaultOption(inputOptions, option):
                if option == 'plugins_specific':
                    mergeOption = mergeOption.split()
                elif option in ('max_level', 'pool_size', 'timeout', 'log_level'):
                    mergeOption = int(mergeOption)

                inputOptions[option] = mergeOption


def _isDefaultOption(inputOptions, option):
    defaultOptions = {
        'plugins_specific': None,
        'max_level': 4,
        'timeout': 10,
        'pool_size': 500,
        'output_format': 'csv',
        'output_file': None,
        'log_file': None,
        'log_level': 1,
        'proxy_file': None,
        'verify_proxy': False,
        'alive_check': False,
    }
    return inputOptions[option] == defaultOptions[option]
