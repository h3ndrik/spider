#!/usr/bin/env python3
# coding: utf-8

import logging
import os
import imp

logger = logging.getLogger(__name__)

class PluginLoader(object):
    """Plugin Loader"""

    def __init__(self):
        self.plugindir = "./plugins"

    def getPlugins(self):
        plugins = []
        for plugin in os.listdir(PluginDirectory):
            location = os.path.join(PluginDirectory, i)
            if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(MainModule, [location])
            plugins.append({"name": i, "info": info})
        return plugins

    def loadPlugin(plugin):
        return imp.load_module(MainModule, *plugin["info"])


    for i in pluginloader.getPlugins():
        print("Loading plugin " + i["name"])
        plugin = pluginloader.loadPlugin(i)
        plugin.run()
