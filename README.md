## Application Builder

The goal of application builder is to have a single object that connects `settings` and the current application `environment` in one place. This object can then be used throughout your python application,
as a central spot for checking which environment the application is running under and for gettings settings accordingly. 


## Usage Example

```python
from application_builder.application import Application

# our settings class must support 2 functions `load()` and `settings()`.

class MySettingsManager:

    def __init__(self, env, app_root):
        self._env = env
        self._root = app_root

    def load(self):
        # json/yaml/python files could be loaded here
        self._data = { 
            'test' : { 'db' : 'localhost' },
            'dev' : { 'db' : 'some.server.com' }
        }

    def settings(self):
        return self._data

def settings_init_fn(env: str, app_root: str):
    sm = MySettingsManager(env, app_root)
    return sm

# Let's assume MYAPP_ENV='dev'

myapp = Application(
    name = 'myapp',
    app_env_varname: 'MYAPP_ENV',
    app_root_dir: '/path/to/myapp',

    # sometimes you might need to do a lot more
    # than just instantiate a class, that's why you need to pass a function
    settings_class_init_fn: settings_init_fn
)

myapp.add_path('settings', 'config/settings')
myapp.add_path('data', 'data')

myapp.boot()

myapp.current_environment() # 'dev'

myapp.settings() # { 'db' : 'some.server.com' }

myapp.paths('root') # /path/to/myapp
myapp.paths('settings') # /path/to/myapp/config/settings
myapp.paths('data') # /path/to/myapp/data
```