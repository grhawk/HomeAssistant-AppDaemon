from typing import List, Coroutine

import appdaemon.plugins.hass.hassapi as hass
from appdaemon.entity import Entity


class SmartSwitchSingleDouble(hass.Hass):
    _handles: List[Coroutine]
    _counter: int
    _single_click_lights: List[Entity]
    _run_in_handle = None
    delay = .8

    def log(self, msg, level="INFO"):
        super().log(__class__.__name__ + ": " + msg, level=level)

    def initialize(self):
        self.log("SmartSwitch initialized")
        self._counter = 0
        self._handles = [self.listen_state(self.switch_lights, i) for i in self.args["switches"]]
        self.entities_single = [self.get_entity(i) for i in self.args["lights.single"]]
        self.entities_double = [self.get_entity(i) for i in self.args["lights.double"]]
        self.delay = float(self.args["delay"])

    def switch_lights(self, entity, attribute, old, new, kwargs):
        if self._counter == 1:
            if self._run_in_handle is not None:
                self.cancel_timer(self._run_in_handle)
            self.run_in(self._double_click, 0)
        elif self._counter == 0:
            self._run_in_handle = self.run_in(self._single_click, self.delay)
            self._counter += 1

    def _double_click(self, cb_kwargs=None):
        self.log(">>>>>>>>>>>>>>> double click <<<<<<<<<<<<<<<<<<<")
        self._counter = 0
        self._run_in_handle = None
        self._toggle_on_double()

    def _single_click(self, cb_kwargs=None):
        self.log(">>>>>>>>>>>>>>> single click <<<<<<<<<<<<<<<<<<<")
        self._counter = 0
        self._run_in_handle = None
        self._toggle_on_single()

    def _toggle_on_single(self):
        if any([entity for entity in self.entities_single if self.get_state(entity.entity_id) == "on"]):
            toggle = self.turn_off
        else:
            toggle = self.turn_on

        for entity in self.entities_single:
            toggle(entity.entity_id)

    def _toggle_on_double(self):
        if any([entity for entity in self.entities_double if self.get_state(entity.entity_id) == "on"]):
            toggle = self.turn_off
        else:
            toggle = self.turn_on
        for entity in self.entities_double:
            toggle(entity.entity_id)
