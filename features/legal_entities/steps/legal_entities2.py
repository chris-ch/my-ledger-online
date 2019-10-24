from lettuce import step, world

from aloe.parser import Step

@step("User \'(.*)\' is in the system")
def step_impl(step_instance: Step, username: str):
    """
    :type step_instance: lettuce.core.Step
    """
    raise NotImplementedError(u'STEP: Given User \'aqua\' is in the system')