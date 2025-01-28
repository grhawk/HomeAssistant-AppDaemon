from typing import Coroutine, List

import appdaemon.adapi
import hassapi as hass


class RotarySmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handles_toggle: List[Coroutine] = []

    def initialize(self):
        for rotary_switch in self.args["rotary_switches"]:
            self.handles_toggle.append(self.listen_state(self.toggle_callback, rotary_switch["action"], new="toggle"))
            self.handles_toggle.append(self.listen_state(self.toggle_callback_hold, rotary_switch["action"], new="hue_move"))

    def toggle_callback(self, entity, attribute, old, new, kwargs):
        self.toggle(self.args["light"])

    def toggle_callback_hold(self,entity, attribute, old, new, kwargs):
        self.toggle(self.args["light_hold"])