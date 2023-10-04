import time
from typing import List

import pytest


class TestDoubleClick:

    lights_single_click: List[str] = ['light.virtual_double_click_1', 'light.virtual_double_click_2']
    lights_double_click: List[str] = ['light.virtual_single_click_1', 'light.virtual_single_click_2']
    switch: List[str] = ['switch.virtual_single_double_switch']
    lights: List[str] = lights_single_click + lights_double_click

    @pytest.fixture()
    def all_off(self, hoass_api):
        hoass_api.set_state_for_all(self.switch, 'off')
        hoass_api.set_state_for_all(self.lights, 'off')
        time.sleep(1)
        yield None
        time.sleep(1)

    @pytest.fixture()
    def all_on(self, hoass_api):
        hoass_api.set_state_for_all(self.switch, 'on')
        hoass_api.set_state_for_all(self.lights, 'on')
        time.sleep(1)

    @pytest.fixture()
    def single_click_on(self, hoass_api, all_off):
        hoass_api.set_state(self.switch[0], "on")
        hoass_api.set_state_for_all(self.lights_single_click, "on")
        time.sleep(1)

    @pytest.fixture()
    def double_click_on(self, hoass_api, all_off):
        hoass_api.set_state_for_all(self.lights_double_click, "on")
        time.sleep(1)

    def test_single_click_on(self, hoass_api, all_off):
        # Turn on light single click
        hoass_api.set_state(self.switch[0], "on")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_single_click_off(self, hoass_api, single_click_on):
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'off')

    def test_double_click_on(self, hoass_api, all_off):
        # Turn on light double click
        hoass_api.set_state(self.switch[0], "on")
        time.sleep(0.3)
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_double_click, 'on')
        hoass_api.assert_state_is(self.lights_single_click, 'off')

    def test_double_click_off(self, hoass_api, double_click_on):
        # Turn on light single click when double click is on
        hoass_api.set_state(self.switch[0], "on")
        time.sleep(0.3)
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'off')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_double_click_on_after_single_click_on(self, hoass_api, single_click_on):
        # Turn off light double click when single click is on
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(0.3)
        hoass_api.set_state(self.switch[0], "on")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'on')

    def test_double_click_off_after_single_click_on(self, hoass_api, all_on):
        # Turn off all with a single click when both lights are on
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(0.3)
        hoass_api.set_state(self.switch[0], "on")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_single_click_after_all_on_is_all_off(self, hoass_api, all_on):
        hoass_api.set_state(self.switch[0], "off")
        time.sleep(1)
        hoass_api.assert_state_is(self.lights_single_click, 'off')
        hoass_api.assert_state_is(self.lights_double_click, 'off')
