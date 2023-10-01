import time

from requests import post
from requests import get


class HoassApi:

    def __init__(self):
        self.base_url = "http://localhost:8123/api/states/"
        self.headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmZWVhNjc1YTZmOTY0YjNlYmRjNzBhMjIzMzVmMzVjZSIsImlhdCI6MTY5NDYyMTYwMCwiZXhwIjoyMDA5OTgxNjAwfQ.C1Fdiof3_r6d9vv0zuNb8CZr5BYhDuJV6PSH68vFXhA",
            "content-type": "application/json",
        }

    def hass_get_entity(self, entity: str) -> dict:
        response = get(self.base_url + entity, headers=self.headers)
        assert response.status_code == 200
        return response.json()

    def assert_state_is(self, entity: str, state: str):
        response = self.hass_get_entity(entity)
        assert response['state'] == state


def test_turn_on_off_switch():
    base_url = "http://localhost:8123/api/states/"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmZWVhNjc1YTZmOTY0YjNlYmRjNzBhMjIzMzVmMzVjZSIsImlhdCI6MTY5NDYyMTYwMCwiZXhwIjoyMDA5OTgxNjAwfQ.C1Fdiof3_r6d9vv0zuNb8CZr5BYhDuJV6PSH68vFXhA",
        "content-type": "application/json",
    }

    light = 'light.virtual_light_1'

    HoassApi().assert_state_is(light, 'off')
    response = post(base_url + 'switch.virtual_switch_1', headers=headers, data='{"state": "on"}')
    assert response.status_code == 200
    assert response.json()['state'] == 'on'
    time.sleep(1)
    response = post(base_url + 'switch.virtual_switch_1', headers=headers, data='{"state": "off"}')
    assert response.status_code == 200
    assert response.json()['state'] == 'off'
    time.sleep(1)
    final_light_state = get(base_url + 'light.virtual_light_1', headers=headers)
    assert final_light_state.status_code == 200
    assert final_light_state.json()['state'] == 'off'