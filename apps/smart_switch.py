from typing import Coroutine, List

import appdaemon.adapi
import hassapi as hass
from appdaemon.entity import Entity


class SmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handles: List[Coroutine]
    counter: int
    entities: List[Entity]

    def log(self, msg, level="INFO"):
        super().log(__class__.__name__ + ": " + msg, level=level)

    def initialize(self):
        self.log("SmartSwitch initialized")
        self.counter = 0
        self.handles = [self.listen_state(self.switch_lights, i) for i in self.args["switch"]]
        self.entities = [self.get_entity(i) for i in self.args["lights"]]

    # def set_day_scene(self, entity, attribute, old, new, kwargs):
    #     self.log("set_day_scene")
    #     delay = 2
    #     self.log("Counter: " + str(self.counter))
    #     if self.counter == 0:
    #         self.log("Counter: " + str(self.counter))
    #         self.counter += 1
    #         self.handle = self.run_in(self.switch_lights(entity, attribute, old, new, kwargs), delay)
    #         self.counter = 0
    #     elif self.counter == 1:
    #         self.cancel_timer(self.handle)
    #         self.counter += 1
    #         self.log("Counter: " + str(self.counter))
    #         self.day_scene("test")
    #         self.counter = 0
    #     self.log("end set_day_scene")

    def switch_lights(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log(">>>>>>>>>>>>>Turning on lights<<<<<<<<<<<<<<<<<<<")
            if self.sun_up():
                self._day_scene()
            else:
                self._night_scene()
        else:
            self.log(">>>>>>>>>>>>>Turning off lights<<<<<<<<<<<<<<<<<<<")
            for ent in self.entities:
                ent.turn_off()

    def _day_scene(self):
        self.log("day_scene")
        for entity in self.entities:
            entity.turn_on(brightness=255, color_temp=1, transition=2)
        self.log("end day_scene")

    def _night_scene(self):
        self.log("night_scene")
        for entity in self.entities:
            entity.turn_on(brightness=255, color_temp=500, transition=2)
        self.log("end night_scene")
