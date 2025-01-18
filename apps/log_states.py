from typing import Coroutine

import appdaemon.adapi
import hassapi as hass


class LogStates(hass.Hass, appdaemon.adapi.ADAPI):
    handle: Coroutine

    def log(self, msg: str, level="INFO", **kwargs) -> None:
        super().log(__class__.__name__ + ": " + msg, level=level, **kwargs)

    def initialize(self):
        self.log("LogStates initialized")
        self.handle = [self.listen_state(self.log_state, i) for i in self.args["entities_id"]]

    def log_state(self, entity, attribute, old, new, kwargs):
        self.log("---------------------------------------------")
        self.log(">>>>>>>>>>>State changed end<<<<<<<<<<<<<<<<<")
        self.log("state: " + str(self.get_entity(entity).get_state(entity)))
        self.log("attribute: " + str(attribute))
        self.log("kwargs: " + str(kwargs))
        self.log("new #" + new + "#")
        self.log("old #" + old + "#")
        self.log("Entity: " + entity)
        self.log(">>>>>>>>>>>>>State changed<<<<<<<<<<<<<<<<<<<")
        self.log("---------------------------------------------")



