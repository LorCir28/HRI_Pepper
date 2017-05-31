import time
import signal
import argparse
from naoqi import ALProxy, ALBroker, ALModule
from abc import ABCMeta
import os

class EventAbstractClass(ALModule):
    __metaclass__ = ABCMeta

    def __init__(self, name, ip, port):
        self.name = name
        self._make_global(self.name, self)
        self.broker = self._connect(name, ip, port)
        super(EventAbstractClass, self).__init__(self.name)

        self.memory = self._make_global("memory", ALProxy("ALMemory"))

    def _connect(self, name, ip, port):
        try:
            broker = ALBroker("speech_broker",
               "0.0.0.0",   # listen to anyone
               0,           # find a free port and use it
               ip,         # parent broker IP
               port)
            print "Connected to %s:%s" % (ip, str(port))
            return broker
        except RuntimeError:
            print "Cannot connect to %s:%s. Retrying in 1 second." % (ip, str(port))
            time.sleep(1)
            return self._connect(name, ip, port)

    def _make_global(self, name, var):
        globals()[name] = var
        return globals()[name]

    def subscribe(self, event, callback):
    	from speech_recognition import SpeechRecognition
    	self.memory.subscribeToEvent(
            event,
            self.name,
            callback.func_name
        )

    def unsubscribe(self, event):
        self.memory.unsubscribeToEvent(
            event,
            self.name
        )

    def remove_subscribers(self, event):
        subscribers = self.memory.getSubscribers(event)
        if subscribers:
            print "Speech recognition already in use by another node"
            for module in subscribers:
                self.__stop_module(module, event)

    def __stop_module(self, module, event):
        print "Unsubscribing '{}' from NAO speech recognition".format(
            module)
        try:
            self.memory.unsubscribeToEvent(event, module)
        except RuntimeError:
            print "Could not unsubscribe from NAO speech recognition"
