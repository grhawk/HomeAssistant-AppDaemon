import time
from typing import List

import pytest

SWITCHES: List[str] = ['switch.virtual_switch_1', 'switch.virtual_switch_2']


def test_turn_on_off_switch(hoass_api):

    lights: List[str] = ['light.virtual_light_1', 'light.virtual_light_2']

    hoass_api.set_state_for_all(lights, 'off')
    hoass_api.set_state_for_all(SWITCHES, 'off')

    # Turn on light from Switch 1
    hoass_api.assert_state_is(lights, 'off')
    hoass_api.set_state(SWITCHES[0], "on")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'on')

    # Turn off light
    hoass_api.set_state(SWITCHES[0], "off")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'off')

    # Turn on light from Switch 2
    hoass_api.set_state(SWITCHES[1], "on")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'on')

    # Turn off light
    hoass_api.set_state(SWITCHES[1], "off")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'off')

@pytest.mark.skip(reason="not implemented")
def test_double_toggle(hoass_api):

    light_always_off = 'light.virtual_light_1'
    light_toggling = 'light.virtual_light_2'
    hoass_api.assert_state_is(light_toggling, 'off')
    hoass_api.assert_state_is(light_always_off, 'off')

    # Turn on light
    hoass_api.set_state(SWITCH, "on")
    time.sleep(0.3)
    hoass_api.set_state(SWITCH, "off")
    time.sleep(1)
    hoass_api.assert_state_is(light_toggling, 'on')
    hoass_api.assert_state_is(light_always_off, 'off')
    time.sleep(1)

    # Turn off light
    hoass_api.set_state(SWITCH, "on")
    time.sleep(0.3)
    hoass_api.set_state(SWITCH, "off")
    time.sleep(1)
    hoass_api.assert_state_is(light_toggling, 'off')
    hoass_api.assert_state_is(light_always_off, 'off')
