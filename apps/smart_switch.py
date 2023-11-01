from typing import Coroutine, List

import appdaemon.adapi
import hassapi as hass
from appdaemon.entity import Entity


class SmartSwitch(hass.Hass, appdaemon.adapi.ADAPI):
    handles: List[Coroutine]
    counter: int
    entities: List[Entity]
    transition_time: int = 2
    transition_time_off: int = 2
    _handle_turn_off: str
    _handle_turn_on: str

    def log(self, msg, level="INFO"):
        super().log(__class__.__name__ + ": " + msg, level=level)

    def initialize(self):
        self.log("SmartSwitch initialized")
        self.counter = 0
        self.handles = [self.listen_state(self.switch_lights, i) for i in self.args["switches"]]
        self.entities = [self.get_entity(i) for i in self.args["lights"]]
        self._handle_turn_off: str = None
        self._handle_turn_on: str = None

    def switch_lights(self, entity, attribute, old, new, kwargs):

        if self._handle_turn_off is not None:
            self.cancel_sequence(self._handle_turn_off)
            self._handle_turn_off = None
        if self._handle_turn_on is not None:
            self.cancel_timer(self._handle_turn_on)
            self._handle_turn_on = None
        if new == "on":
            self.log(">>>>>>>>>>>>>Turning on lights<<<<<<<<<<<<<<<<<<<")
            if self.sun_up():
                self._day_scene()
            else:
                self._night_scene()
        else:
            self.log(">>>>>>>>>>>>>Turning off lights<<<<<<<<<<<<<<<<<<<")
            sequence = [{"light/turn_on": {"brightness": 1, "transition": self.transition_time_off}},
                        {"sleep": self.transition_time_off+0.2},
                        {"light/turn_off": {}}]
            final_sequence = []
            for ent in self.entities:
                for step in sequence:
                    for k, v in step.items():
                        if k == "sleep":
                            final_sequence.append({k: v})
                        else:
                            final_sequence.append({k: {"entity_id": ent.entity_id, **v}})

            self._handle_turn_off = self.run_sequence(final_sequence)

    def _day_scene(self):
        self.log("day_scene")
        for entity in self.entities:
            entity.turn_on(brightness=255, color_temp=1, transition=self.transition_time)
        self.log("end day_scene")

    def _night_scene(self):
        self.log("night_scene")
        for entity in self.entities:
            self._handle_turn_on = entity.turn_on(brightness=255, color_temp=450, transition=self.transition_time)
        self._handle_turn_on = None
        self.log("end night_scene")

