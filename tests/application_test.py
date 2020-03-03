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

def basic_settings_init_fn(env, app_root_dir):
    return BasicSettingsManager(env, app_root_dir)
        

def test_application():

    # setup env
    os.environ['TEST1_ENV'] = 'test'

    k = app.Application(
        name='test1',
        app_env_varname='TEST1_ENV',
        app_root_dir = '/foo/bar',
        settings_class_init_fn = basic_settings_init_fn
    )

    k.boot()

    assert len(k.settings()) == 3
    assert k.settings()['name'] == 'basic-test'
    assert k.settings()['db'] == 'test'
    assert k.settings()['test_param'] == 800
    assert k.current_environment() == 'test'
    assert k.paths('root') == '/foo/bar'

    # shutdown
    del os.environ['TEST1_ENV']

def test_paths():

    os.environ['T2_PATH_ENV'] = 'dev'

    k = app.Application(
        name = 'path_test',
        app_env_varname = 'T2_PATH_ENV',
        app_root_dir = '/app/base/path',
        settings_class_init_fn = basic_settings_init_fn
    )

    k.boot()

    k.add_path('config', 'config/settings/app_settings')
    k.add_path('eggs', 'data/eggs')
    k.add_path('external_data', '/var/etc/lib/data', append_to_root = False)

    assert k.paths('root') == '/app/base/path'
    assert k.paths('config') == '/app/base/path/config/settings/app_settings'
    assert k.paths('eggs') == '/app/base/path/data/eggs'
    assert k.paths('external_data') == '/var/etc/lib/data'

    with pytest.raises(Exception, match=r'Cannot override application root path'):
        k.add_path('root', '/cant/override')

    with pytest.raises(Exception, match=r'Cannot append paths prefixed with `/` to application root'):
        k.add_path('config', '/cant/append/to/root/as/absolute_path')

    del os.environ['T2_PATH_ENV']