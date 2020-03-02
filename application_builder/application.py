from typing import (
    Protocol,
    Callable,
    Dict,
    Any
)

import os

class EnvironmentVariable(object):

    def __init__(self, name: str):
        self._name = name

    def name(self):
        return self._name

    def get(self):
        value = os.getenv(self._name)
        
        if not value:
            raise Exception('Environment variable `{}` not set'.format(self._name))
        
        return value

class IApplicationSettingsHandler(Protocol):

    def load(self) -> None:
        pass

    def settings(self) -> Dict[str, Any]:
        pass


class Application(object):

    def __init__(
        self,
        name: str,
        app_env_varname: str,
        app_root_dir: str,
        settings_class_init_fn: Callable[[str, str], IApplicationSettingsHandler]
    ):
        self._name = name
        self._app_envvar = EnvironmentVariable(app_env_varname)
        self._app_root_dir = app_root_dir
        self._paths = { 'root' : app_root_dir }
        self._environment = None
        self._settings_class_init_fn = settings_class_init_fn
        self._settings = None
        self._booted = False

    def boot(self):
        self._environment = self._load_environment()
        self._settings = self._settings_class_init_fn(
            self._environment,
            self._app_root_dir
        )
        self._settings.load()
        self._booted = True

    def current_environment(self):
        return self._environment

    def settings(self):
        return self._settings.settings()

    def root_dir(self):
        return self._app_root_dir

    def add_path(self, pathname: str, pathpart):
        if pathname == 'root':
            raise Exception('cannot override application root path!')

        self._paths[pathname] = os.path.join(self.root_dir(), pathpart)

    def paths(name: str = None) -> Union[Dict[str,str], str]:
        if name:
            return self._paths[name]
        else:
            return self._paths

    def _load_environment(self):
        return self._app_envvar.get()