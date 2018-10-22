from aloe import step, world
from nose.tools import assert_equals
import requests
import json


@step("User \'(.*)\' is in the system")
def step_impl(step_def, username):
    """
    :type step_def: aloe.parser.Step
    """
    raise NotImplementedError(u'STEP: Given User \'aqua\' is in the system')


@step("\'(.*)\' creates the legal entity \'(.*)\'")
def step_impl(step_def):
    """
    :type step_def: aloe.parser.Step
    """
    raise NotImplementedError(u'STEP: When \'aqua\' creates the legal entity \'Aqua corp.\'')


@step("I should get a \'(.*)\' response")
def step_impl(step_def, expected_status_code):
    """
    :type step_def: aloe.parser.Step
    :type expected_status_code: int
    """
    assert_equals(world.response.status_code, int(expected_status_code))


@step("\'(.*)\' should see legal entity \'(.*)\'")
def step_impl(step_def):
    """
    :type step_def: aloe.parser.Step
    """
    raise NotImplementedError(u'STEP: And \'aqua\' should see legal entity \'Aqua corp.\'')


@step("\'(.*)\' should not see legal entity \'(.*)\'")
def step_impl(step_def):
    """
    :type step_def: aloe.parser.Step
    """
    raise NotImplementedError(u'STEP: And \'aqua\' should not see legal entity \'Blue & Associates\'')
