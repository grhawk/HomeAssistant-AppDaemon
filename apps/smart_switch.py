from typing import Coroutine, List

import appdaemon.adapi
import hassapi as hass
from appdaemon.entity import Entity


class SmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handles: List[Coroutine]
    counter: int
    entities: List[Entity]
    transition_time: int = 2
    _handle_turn_off: str

    def log(self, msg, level="INFO"):
        super().log(__class__.__name__ + ": " + msg, level=level)

    def initialize(self):
        self.log("SmartSwitch initialized")
        self.counter = 0
        self.handles = [self.listen_state(self.switch_lights, i) for i in self.args["switches"]]
        self.entities = [self.get_entity(i) for i in self.args["lights"]]

    def switch_lights(self, entity, attribute, old, new, kwargs):
        if self.timer_running(self._handle_turn_off):
            self.cancel_timer(self._handle_turn_off)
        if new == "on":
            self.log(">>>>>>>>>>>>>Turning on lights<<<<<<<<<<<<<<<<<<<")
            if self.sun_up():
                self._day_scene()
            else:
                self._night_scene()
        else:
            self.log(">>>>>>>>>>>>>Turning off lights<<<<<<<<<<<<<<<<<<<")
            self._handle_turn_off = self.run_in(self._turn_off, self.transition_time+1)
            for ent in self.entities:
                ent.set_state(brightness=1, transition=self.transition_time)

    def _turn_off(self):
        for ent in self.entities:
            ent.turn_off()

    def _day_scene(self):
        self.log("day_scene")
        for entity in self.entities:
            entity.turn_on(brightness=255, color_temp=1, transition=self.transition_time)
        self.log("end day_scene")

    def _night_scene(self):
        self.log("night_scene")
        for entity in self.entities:
            entity.turn_on(brightness=255, color_temp=450, transition=self.transition_time)
        self.log("end night_scene")
