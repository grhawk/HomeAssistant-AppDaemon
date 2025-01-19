from typing import Coroutine

from appdaemon import appdaemon
from appdaemon.plugins import hass


class RotarySmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handle: Coroutine

    def initialize(self):
        handle_toggle = self.listen_state(self.toggle_callback, self.args["rotary_switches"]["action"], new="toggle")

    def toggle_callback(self, entity, attribute, old, new, kwargs):
        self.toggle(self.args["light"])
