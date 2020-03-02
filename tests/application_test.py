import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import application_builder.application as app

class BasicSettingsManager:

    def __init__(self, env: str, root_dir: str):
        self._env = env
        self._root_dir = root_dir
        self._data = {}

    def load(self):
        self._data = {
            'test' : { 'name' : 'basic-test', 'db' : 'test', 'test_param' : 800 },
            'dev' : { 'name' : 'basic-dev', 'db' : 'dev', 'dev_param' : 1000 }
        }

    def settings(self):
        return self._data[self._env]
        

def test_simple_application():

    # setup env
    os.environ['TEST1_ENV'] = 'test'

    init_fn = lambda env, app_root_dir: BasicSettingsManager(env, app_root_dir)

    k = app.Application(
        name='test1',
        app_env_varname='TEST1_ENV',
        app_root_dir = '/foo/bar',
        settings_class_init_fn = init_fn
    )

    k.boot()

    assert len(k.settings()) == 3
    assert k.settings()['name'] == 'basic-test'
    assert k.settings()['db'] == 'test'
    assert k.settings()['test_param'] == 800
    assert k.current_environment() == 'test'

    # shutdown
    del os.environ['TEST1_ENV']