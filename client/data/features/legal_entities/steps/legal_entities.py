import aloe
from aloe import step, world, before, after
from aloe.parser import Step
from nose.tools import assert_equals
import json
import logging
import requests

_srv = None
_host = 'django'
_port = 8000


def uri(path):
    uri_value = 'http://%s:%s/%s' % (_host, _port, path)
    logging.info('building uri: %s', uri_value)
    return uri_value


def connect():
    world.session = requests.Session()
    world.session.auth = ('oas', 'oas')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic b2FzOm9hcw==',
        'Cache-Control': 'no-cache',
        'Postman-Token': '8fb9cf48-e7aa-4135-bd9f-306349e4a180'
    }
    world.session.headers.update(headers)


@after.all
def release():
    pass


@step("User \'(.*)\' is in the system")
def step_impl(step_def: Step, username: str):
    logging.info('creating user %s', username)
    payload = {
        'code': '%s' % username,
        'username': '%s' % username,
        'email': '%s@test.test' % username,
        'legal_entities': []
    }
    res = world.session.post(uri('users.json'), data=json.dumps(payload))
    logging.info('response status: %s', res.status_code)
    logging.info('response: %s', json.loads(res.text))


@step("\'(.*)\' creates the legal entity \'(.*)\'")
def step_impl(step_def: Step, username: str, legal_entity_code: str):
    logging.info('creating legal entity %s for user %s', legal_entity_code, username)
    payload = {
        'code': '%s' % legal_entity_code,
        'name': '%s' % legal_entity_code,
        'is_individual': 0,
        'currency': 'EUR',
        'user': username,
        'description': 'test'
    }
    world.response = world.session.post(uri('legal_entities.json'), data=json.dumps(payload))
    logging.info('response status: %s', world.response.status_code)
    logging.info('response: %s', json.loads(world.response.text))


@step("I should get a \'(.*)\' response")
def step_impl(step_def: Step, expected_status_code: int):
    assert_equals(world.response.status_code, int(expected_status_code))


@step("\'(.*)\' should see legal entity \'(.*)\'")
def step_impl(step_def: Step, username: str, legal_entity_code: str):
    logging.info('loading legal entities for user %s', username)
    world.response = world.session.get(uri('legal_entities.json'))
    logging.info('response status: %s', world.response.status_code)
    logging.info('response: %s', json.loads(world.response.text))


@step("\'(.*)\' should not see legal entity \'(.*)\'")
def step_impl(step_def: Step):
    raise NotImplementedError(u'STEP: And \'aqua\' should not see legal entity \'Blue & Associates\'')
