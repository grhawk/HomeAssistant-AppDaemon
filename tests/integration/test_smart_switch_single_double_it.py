import time
from typing import List

import pytest


class TestDoubleClick:

    general_delay = 1
    delay_between_clicks = 0.3
    delay_between_checks = 1.2
    lights_double_click: List[str] = ['light.virtual_double_click_1', 'light.virtual_double_click_2']
    lights_single_click: List[str] = ['light.virtual_single_click_1', 'light.virtual_single_click_2']
    switch: List[str] = ['switch.virtual_switch_single_double']
    lights: List[str] = lights_single_click + lights_double_click

    @pytest.fixture()
    def all_off(self, hoass_api):
        hoass_api.call_service_for_all(self.lights, 'off')
        # hoass_api.call_service_for_all(self.switch, 'off')
        time.sleep(self.general_delay)
        yield None
        time.sleep(self.general_delay)

    @pytest.fixture()
    def all_on(self, hoass_api):
        # hoass_api.call_service_for_all(self.switch, 'on')
        hoass_api.call_service_for_all(self.lights, 'on')
        time.sleep(self.general_delay)

    @pytest.fixture()
    def single_click_on(self, hoass_api, all_off):
        # hoass_api.call_service(self.switch[0], "on")
        hoass_api.call_service_for_all(self.lights_single_click, "on")
        time.sleep(self.general_delay)

    @pytest.fixture()
    def double_click_on(self, hoass_api, all_off):
        hoass_api.call_service_for_all(self.lights_double_click, "on")
        time.sleep(self.general_delay)

    def test_single_click_on(self, hoass_api, all_off):
        # Turn on light single click
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_single_click_off(self, hoass_api, single_click_on):
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'off')

    def test_double_click_on(self, hoass_api, all_off):
        # Turn on light double click
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_clicks)
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_double_click, 'on')
        hoass_api.assert_state_is(self.lights_single_click, 'off')

    def test_double_click_off(self, hoass_api, double_click_on):
        # Turn on light single click when double click is on
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_clicks)
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'off')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_double_click_on_after_single_click_on(self, hoass_api, single_click_on):
        # Turn off light double click when single click is on
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_clicks)
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'on')

    def test_double_click_off_after_single_click_on(self, hoass_api, all_on):
        # Turn off all with a single click when both lights are on
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_clicks)
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'on')
        hoass_api.assert_state_is(self.lights_double_click, 'off')

    def test_single_click_after_all_on(self, hoass_api, all_on):
        hoass_api.call_service(self.switch[0], "toggle")
        time.sleep(self.delay_between_checks)
        hoass_api.assert_state_is(self.lights_single_click, 'off')
        hoass_api.assert_state_is(self.lights_double_click, 'on')
