from unittest import mock

from appdaemon_testing.pytest import automation_fixture

from apps.smart_switch_single_double import SmartSwitchSingleDouble

class TestSmartSwitchSingleDoubleUt:

    @automation_fixture(
        SmartSwitchSingleDouble,
        args={'switches': ['switch.smart_sd'],
              'lights.single': ['light.single_1', 'light.single_2'],
              'lights.double': ['light.double_1', 'light.double_2']}
                        )
    def automation(self) -> SmartSwitchSingleDouble:
        # Provides the automation using the fixture
        pass

    def test_initialize(self, hass_driver, automation: SmartSwitchSingleDouble):
        listen_state = hass_driver.get_mock('listen_state')
        listen_state.assert_called_once_with(automation.switch_lights, 'switch.smart_sd')

    def test_single_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        hass_driver.set_state('switch.smart_sd', 'on')

        run_in_m = hass_driver.get_mock('run_in')
        assert run_in_m.call_count == 1
        run_in_m.assert_called_once_with(automation._single_click, automation.delay)

    def test_double_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        hass_driver.set_state('switch.smart_sd', 'on')
        hass_driver.set_state('switch.smart_sd', 'off')

        run_in_m = hass_driver.get_mock('run_in')
        assert run_in_m.call_count == 2
        run_in_m.assert_has_calls([mock.call(automation._single_click, automation.delay), mock.call(automation._double_click, 0)])

        cancel_timer_m = hass_driver.get_mock('cancel_timer')
        assert cancel_timer_m.call_count == 1
        cancel_timer_m.assert_called_once_with(automation._run_in_handle)

    def test_turn_on_single_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        automation._single_click()

        turn_on_m = hass_driver.get_mock('turn_on')
        assert turn_on_m.call_count == 2
        turn_on_m.assert_has_calls([mock.call('light.single_1'), mock.call('light.single_2')])

    def test_turn_off_single_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'on')
            hass_driver.set_state('light.single_1', 'on')
            hass_driver.set_state('light.single_2', 'on')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        automation._single_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.single_1'), mock.call('light.single_2')])

    def test_turn_off_single_click_with_only_light_1_on(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'on')
            hass_driver.set_state('light.single_1', 'on')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        automation._single_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.single_1'), mock.call('light.single_2')])

    def test_turn_off_single_click_with_only_light_2_on(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'on')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'on')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        automation._single_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.single_1'), mock.call('light.single_2')])

    def test_turn_on_double_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'off')

        automation._double_click()

        turn_on_m = hass_driver.get_mock('turn_on')
        assert turn_on_m.call_count == 2
        turn_on_m.assert_has_calls([mock.call('light.double_1'), mock.call('light.double_2')])

    def test_turn_off_double_click(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'on')
            hass_driver.set_state('light.double_2', 'on')

        automation._double_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.double_1'), mock.call('light.double_2')])

    def test_turn_off_double_click_with_light_2_on(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'off')
            hass_driver.set_state('light.double_2', 'on')

        automation._double_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.double_1'), mock.call('light.double_2')])

    def test_turn_off_double_click_with_light_1_on(self, hass_driver, automation: SmartSwitchSingleDouble):
        with hass_driver.setup():
            hass_driver.set_state('switch.smart_sd', 'off')
            hass_driver.set_state('light.single_1', 'off')
            hass_driver.set_state('light.single_2', 'off')
            hass_driver.set_state('light.double_1', 'on')
            hass_driver.set_state('light.double_2', 'off')

        automation._double_click()

        turn_off_m = hass_driver.get_mock('turn_off')
        assert turn_off_m.call_count == 2
        turn_off_m.assert_has_calls([mock.call('light.double_1'), mock.call('light.double_2')])