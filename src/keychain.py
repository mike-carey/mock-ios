###
#
##

import os
import sys
import json

from helpers import classproperty

def _get_keychain_file():
    return os.environ.get('KEYCHAIN_FILE', './keychains.json')
# _get_keychain_file

class Keychain(object):
    __keychains__ = {}

    def __init__(self, name, **kwargs):
        self.name = name
        self.locked = kwargs.pop('locked', False)
        self.timeout = kwargs.pop('timeout', -1)
        self.owner = kwargs.pop('owner', None)
        self.default = kwargs.pop('default', False)
        self.password = kwargs.pop('password', None)
        self.lock_on_sleep = kwargs.pop('lock_on_sleep', False)
        self.certificates = [c if isinstance(c, Certificate) else Certificate(**c) for c in kwargs.pop('certificates', [])]

        if len(Keychain.__keychains__) < 1:
            self.default = True
        # fi

        Keychain.__keychains__[self.name] = self
    # __init__

    @classproperty
    def KEYCHAINS(cls):
        data = {}
        for key, val in cls.__keychains__.items():
            data[key] = val.__properties__
        # done

        return data
    # keychains

    @classproperty
    def DEFAULT(cls):
        for k, v in cls.__keychains__.items():
            if v.default is True:
                return v
            # fi
        # done
    # default

    @property
    def __properties__(self):
        return {
            "name": self.name,
            "timeout": self.timeout,
            "owner": self.owner,
            "default": self.default,
            "password": self.password,
            "locked": self.locked,
            "lock_on_sleep": self.lock_on_sleep,
            "certificates": [c.__properties__ for c in self.certificates]
        }
    # __properties__

    def unlock(self, **kwargs):
        if kwargs.pop('password', None) != self.password:
            raise Exception('Password does not match')
        # fi
        self.locked = False
    # unlock

    def lock(self):
        self.locked = True
    # unlock

    def import_certificate(self, filepath, **kwargs):
        self.certificates.append(Certificate(filepath, **kwargs))
    # import_cert

    @classmethod
    def find(cls, name, default=None):
        if name in cls.__keychains__:
            return cls.__keychains__[name]
        # fi

        if default is not None:
            return default
        # fi

        raise Exception('No keychain `%s` found' % name)
    # find


    @classmethod
    def set_default(cls, name):
        default = cls.DEFAULT
        if default is not None:
            default.default = False
        # fi

        cls.find(name).default = True
    # set_default

    @classmethod
    def status(cls):
        print(json.dumps(cls.__dict__))
    # status

    @classmethod
    def load(cls, filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = {}
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    print("Could not decode json for %s.  Moving on" % filename)
                #

                for key, val in data.get('keychains', {}).items():
                    cls.__keychains__[key] = Keychain(**val)
                # done
            # end
        # fi
    # load

    @classmethod
    def save(cls, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump({
                "keychains": cls.KEYCHAINS
            }, f, indent=2)
        # end
    # save

    @classmethod
    def delete(cls, name):
        obj = cls.find(name)
        del cls.__keychains__[obj.name]
    # delete

# Keychain

class Certificate(object):
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.applications = kwargs.pop('applications', [])
        self.passphrase = kwargs.pop('passphrase', None)
    # __init__

    @property
    def __properties__(self):
        return {
            "filepath": self.filepath,
            "applications": self.applications,
            "passphrase": self.passphrase
        }
    # __properties__
# Cert


###
# Utility functions
##

def keychain_decorator(fn):
    def _keychain_decorator(*args, **kwargs):
        Keychain.load(_get_keychain_file())
        value = fn(*args, **kwargs)
        Keychain.save(_get_keychain_file())

        return value
    # _keychain_decorator

    return _keychain_decorator
# keychain_decorator

@keychain_decorator
def create_keychain(name, **kwargs):
    Keychain(name, **kwargs)
# create_keychain

@keychain_decorator
def default_keychain(name, **kwargs):
    Keychain.find(name).default = True
# default_keychain

@keychain_decorator
def delete_keychain(name):
    Keychain.delete(name)
# delete_keychain

@keychain_decorator
def import_keychain():
    pass
# import_keychain

@keychain_decorator
def set_keychain_settings(name, **kwargs):
    keychain = Keychain.find(name)
    for k, v in kwargs.items():
        setattr(keychain, k, v)
    # done
# set_keychain_settings

@keychain_decorator
def unlock_keychain(name, **kwargs):
    Keychain.find(name).unlock(**kwargs)
# unlock_keychain

@keychain_decorator
def lock_keychain(name, **kwargs):
    Keychain.find(name).lock()
# unlock_keychain

@keychain_decorator
def import_certificate(name=None, **kwargs):
    Keychain.find(name, Keychain.DEFAULT).import_certificate(**kwargs)
# import_certificate

if __name__ == '__main__':
    Keychain.load(_get_keychain_file())
    Keychain.status()
# fi

# Keychain
