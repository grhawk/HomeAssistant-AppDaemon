import time

import hassapi as hass

class SmartSwitch(hass.Hass):

    def log(self, msg):
        super().log(__class__.__name__ + ": " + msg, level="INFO")

    def initialize(self):
        self.log("SmartSwitch initialized")
        self.counter = 0
        self.handle = None
        self.listen_state(self.switch_lights, self.args["switch"])
        self.light = self.args["lights"][0]
        # self.listen_state(self.set_day_scene, "switch.living_room_switch_main")

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
                self.day_scene("test")
            else:
                self.night_scene("test")
        else:
            self.log(">>>>>>>>>>>>>Turning off lights<<<<<<<<<<<<<<<<<<<")
            self.turn_off(self.light)

    def day_scene(self, entities: list):
        self.log("day_scene")
        self.turn_on(self.light, brightness=1, color_temp=1, transition=0)
        self.run_in(self.turns_light_on_final, .2, brightness=255, transition=1)
        self.log("end day_scene")

    def turns_light_on_final(self, cb_args):
        self.log("turns_light_on_final")
        self.turn_on(self.light, brightness=cb_args['brightness'], transition=cb_args['transition'])
        self.log("end day_scene")

    def night_scene(self, entities: list):
        self.log("night_scene")
        self.turn_on(self.light, brightness=1, color_temp=500, transition=0)
        self.run_in(self.turns_light_on_final, .2, brightness=255, transition=1)
        self.log("end night_scene")
