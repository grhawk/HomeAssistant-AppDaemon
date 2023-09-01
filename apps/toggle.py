import hassapi as hass

#
# Hello World App
#
# Args:
#


class ToggleLight(hass.Hass):
    def initialize(self):
        self.log("Hello from AppDaemon")
        self.log("You are now ready to run Apps!")
        self.log("Check your logs for details22222222")
        self.log("Is this working?")
        self.listen_state(self.toggle_light, "switch.adguard_home_filtering")

    def toggle_light(self, entity, attribute, old, new, kwargs):
        self.log("toggle_light")
        self.log("entity" + entity)
        self.log("attribute" + attribute)
        self.log("old" + old)
        self.log("new" + new)
        self.log("kwargs" + kwargs)

