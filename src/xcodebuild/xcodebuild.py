###
#
##

import tempfile

from helpers import classproperty, touch
from serialize import Serializable

class Xcodebuild(Serializable):
    @classproperty
    def JSON_KEY(cls):
        return 'xcodebuild'
    # JSON_KEY

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.scheme = kwargs.pop('scheme', None)
        self.sdk = kwargs.pop('sdk', None)
        self.destination = kwargs.pop('destination', None)
        self.configuration = kwargs.pop('configuration', None)

        if len(args) < 1:
            args = kwargs.pop('vars', [])
        # fi

        self.vars = {}
        if len(args) > 0:
            for arg in args:
                key, val = arg.split('=')
                self.vars[key] = val
            # done
        # fi

        Xcodebuild.add(self.project, self)
    # __init__

    def serialize(self):
        return {
            "project": self.project,
            "scheme": self.scheme,
            "sdk": self.sdk,
            "destination": self.destination,
            "configuration": self.configuration,
            "vars": self.vars
        }
    # serialize

# Xcodebuild

@Xcodebuild.decorator
def xcodebuild(*args, **kwargs):
    Xcodebuild(*args, **kwargs)
# xcodebuild

if __name__ == '__main__':
    Xcodebuild.load(Xcodebuild.FILE)
    Xcodebuild.status()
# fi

# xcodebuild.py
