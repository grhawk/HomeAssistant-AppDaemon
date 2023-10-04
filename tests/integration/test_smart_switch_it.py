import time

import pytest

SWITCH = 'switch.virtual_switch_1'


def test_turn_on_off_switch(hoass_api):

    light = 'light.virtual_light_1'
    hoass_api.assert_state_is(light, 'off')
    #TODO: assert state of switch

    # Turn on light
    hoass_api.assert_state_is(light, 'off')
    hoass_api.set_state(SWITCH, "on")
    time.sleep(1)
    hoass_api.assert_state_is(light, 'on')

    # Turn off light
    hoass_api.set_state(SWITCH, "off")
    time.sleep(1)
    hoass_api.assert_state_is(light, 'off')


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
