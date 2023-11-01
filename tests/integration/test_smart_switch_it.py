import time
from typing import List


def test_turn_on_off_switch(hoass_api):

    switches: List[str] = ['switch.virtual_switch_1', 'switch.virtual_switch_2']
    lights: List[str] = ['light.virtual_light_1', 'light.virtual_light_2']

    hoass_api.call_service_for_all(lights, 'off')
    hoass_api.call_service_for_all(switches, 'off')

    # Turn on light from Switch 1
    hoass_api.assert_state_is(lights, 'off')
    hoass_api.call_service(switches[0], "on")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'on')

    # Turn off light
    hoass_api.call_service(switches[0], "off")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'off')

    # Turn on light from Switch 2
    hoass_api.call_service(switches[1], "on")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'on')

    # Turn off light
    hoass_api.call_service(switches[1], "off")
    time.sleep(1)
    hoass_api.assert_state_is(lights, 'off')
