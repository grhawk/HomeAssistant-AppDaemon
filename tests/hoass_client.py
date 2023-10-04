from copy import deepcopy
from typing import List

from requests import get, post, Response, Session, Request


class HoassApi:

    def __init__(self, address: str, port: int):
        self.headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2YTk1NTM2MDJiMGQ0OWRlOGZiMjA1YTBmNDI2MmRjZiIsImlhdCI6MTY5NjQyNjQzNiwiZXhwIjoyMDExNzg2NDM2fQ.TKqIJhMn8pBoYH51STHwYN78qh1OOyIiYNv1MXNkFuU",
            "content-type": "application/json",
        }
        self.s: Session = Session()
        self.s.verify=False
        self.endpoint_base: str = "http://" + address + ":" + str(port) + "/api/"
        self.request: Request = Request(headers=self.headers)
        self.endpoint_states = self.endpoint_base + "states/"

    def status(self) -> Response:
        r: Request = deepcopy(self.request)
        r.method = "GET"
        r.url = self.endpoint_base + "config"
        return self.s.send(r.prepare())

    def hass_get_entity(self, entity: str) -> dict:
        r: Request = deepcopy(self.request)
        r.method = "GET"
        r.url = self.endpoint_states + entity
        response: Response = self.s.send(r.prepare())
        assert response.status_code == 200
        return response.json()

    def assert_state_is(self, entities: List[str], state: str):
        for entity in entities:
            response = self.hass_get_entity(entity)
            assert response['state'] == state

    def assert_state_is_not(self, entities: List[str], state: str):
        for entity in entities:
            response = self.hass_get_entity(entity)
            assert response['state'] != state

    def set_state(self, entity: str, state: str):
        r: Request = deepcopy(self.request)
        r.method = "POST"
        r.url = self.endpoint_states + entity
        r.data = '{"state": "' + state + '"}'
        response: Response = self.s.send(r.prepare())
        assert response.status_code == 200
        assert response.json()['state'] == state

    def set_state_for_all(self, entities: List[str], state: str):
        for entity in entities:
            self.set_state(entity, state)

    def get_state(self, entity: str):
        entity_json = self.hass_get_entity(entity)
        return entity_json['state']
