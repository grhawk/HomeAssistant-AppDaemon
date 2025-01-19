from typing import Coroutine, List

import appdaemon.adapi
import hassapi as hass


class RotarySmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handles_toggle: List[Coroutine] = []

    def initialize(self):
        for rotary_switch in self.args["rotary_switches"]:
            self.handles_toggle.append(self.listen_state(self.toggle_callback, rotary_switch["action"], new="toggle"))

    def toggle_callback(self, entity, attribute, old, new, kwargs):
        self.toggle(self.args["light"])
