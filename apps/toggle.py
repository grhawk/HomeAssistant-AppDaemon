import hassapi as hass

#
# Hello World App
#
# Args:
#
COOLEST = 150
COOL = 250
NEUTRAL = 370
WARM = 454
WARMEST = 500

DARKEST = 5
BRIGHTEST = 255

TEMPERATURES = [COOLEST, COOL, NEUTRAL, WARM, WARMEST]


def _get_next_temperature(actual_temp, param):
    if actual_temp in TEMPERATURES:
        return TEMPERATURES[(TEMPERATURES.index(actual_temp) + param) % len(TEMPERATURES)]
    else:
        return NEUTRAL


class ToggleLight(hass.Hass):

    def initialize(self):
        self.dimmer_switch = self.get_entity(self.args["switch"])
        self.light = self.get_entity(self.args["light"])
        self.handle = self.dimmer_switch.listen_state(self.toggle_light)
        self.counter = 0
        self.dimming_interval = 20
        self.dimming_transition = 1.5

    def toggle_light(self, entity, attribute, old, new, kwargs):
        if __debug__:
            self.log("--------------------EVENT-------------------")
            self.log("entity: " + entity)
            self.log("attribute: " + attribute)
            self.log("old: " + old)
            self.log("new: " + new)
            self.log("kwargs: " + str(kwargs))
            self.log("att: " + str(self.dimmer_switch.attributes))
            self.log("--------------------EVENTEND-------------------")

        self.br = self.light.get_state("brightness")

        if old.endswith("hold_release"):
            self._call_hold_release(old)
            self.counter = 0

        if new.endswith("hold") or old.endswith("hold"):
            self._call_hold(max(new, old))
            self.counter += 1

        if old.endswith("press_release"):
            self._call_on_press(old)
            self.counter = 0

    def _call_hold_release(self, last_action):
        action = last_action.split("_")[0]
        if action == "on":
            self._call_cycle_temperature(action)
        self.log("Action: " + str(action) + " - Counter: " + str(self.counter))

    def _call_on_press(self, action):
        action = action.split("_")[0]
        if action == "up":
            self._call_up(self.dimming_interval)
        elif action == "down":
            self._call_down(self.dimming_interval)
        elif action == "on":
            self._call_on()
        elif action == "off":
            self._call_off()
        self.log("Action: " + str(action) + " - Counter: " + str(self.counter))

    def _call_hold(self, status):
        if status == "up_hold":
            self._set_brightest()
        elif status == "down_hold":
            self._set_darkest()

    def _set_brightest(self):
        self.log("brightest --> br: " + str(self.br))
        self.light.turn_on(brightness=BRIGHTEST, transition=self.dimming_transition)

    def _set_darkest(self):
        self.log("darkest --> br: " + str(self.br))
        self.light.turn_on(brightness=DARKEST, transition=self.dimming_transition)

    def _call_up(self, dimming_interval):
        self.log("up --> br: " + str(self.br))
        self.br = min(self.br + dimming_interval, 255)
        self.light.turn_on(brightness=self.br, transition=self.dimming_transition)

    def _call_down(self, dimming_interval):
        self.log("down --> br: " + str(self.br))
        self.br = max(self.br - dimming_interval, 0)
        self.light.turn_on(brightness=self.br, transition=self.dimming_transition)

    def _call_on(self):
        self.log("on --> br: " + str(self.br))
        self.light.turn_on(transition=self.dimming_transition)

    def _call_off(self):
        self.log("off --> br: " + str(self.br))
        self.light.turn_off(transition=self.dimming_transition)

    def _call_cycle_temperature(self, action):
        cycle_direction = {"on": 1, "off": -1}
        actual_temp = self.light.get_state("color_temp")
        self.log("cycle_temperature --> actual_temp: " + str(actual_temp))
        self.light.turn_on(color_temp=_get_next_temperature(actual_temp, cycle_direction[action]),
                           transition=self.dimming_transition)
