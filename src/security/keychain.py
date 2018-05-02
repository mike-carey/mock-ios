###
#
##

import os
import sys
import json

from helpers import classproperty
from serialize import Serializable

class Keychain(Serializable):
    @classproperty
    def JSON_KEY(cls):
        return 'keychains'
    # JSON_KEY

    def __init__(self, name, **kwargs):
        self.name = name
        self.locked = kwargs.pop('locked', False)
        self.timeout = kwargs.pop('timeout', -1)
        self.owner = kwargs.pop('owner', None)
        self.default = kwargs.pop('default', False)
        self.password = kwargs.pop('password', None)
        self.lock_on_sleep = kwargs.pop('lock_on_sleep', False)
        self.certificates = [c if isinstance(c, Certificate) else Certificate(**c) for c in kwargs.pop('certificates', [])]
        self.partitions = [p if isinstance(p, Partition) else Partition(**p) for p in kwargs.pop('partitions', [])]

        if len(Keychain.INVENTORY) < 1:
            self.default = True
        # fi

        Keychain.add(self.name, self)
    # __init__

    @classproperty
    def DEFAULT(cls):
        for k, v in cls.INVENTORY.items():
            if v.default is True:
                return v
            # fi
        # done
    # default

    def serialize(self):
        return {
            "name": self.name,
            "timeout": self.timeout,
            "owner": self.owner,
            "default": self.default,
            "password": self.password,
            "locked": self.locked,
            "lock_on_sleep": self.lock_on_sleep,
            "certificates": [c.serialize() for c in self.certificates],
            "partitions": [p.serialize() for p in self.partitions]
        }
    # __properties__

    def unlock(self, **kwargs):
        self.check_password(kwargs.pop('password'))
        self.locked = False
    # unlock

    def lock(self):
        self.locked = True
    # unlock

    def check_password(self, password):
        if self.password != password:
            raise Exception("Invalid password")
        # fi
    # check_password

    def import_certificate(self, filepath, **kwargs):
        self.certificates.append(Certificate(filepath, **kwargs))
    # import_cert

    def set_partitions(self, *partition_ids, **kwargs):
        self.check_password(kwargs.pop('password'))
        self.partitions = [Partition(pid, **kwargs) for pid in partition_ids]
    # set_partitions

    @classmethod
    def find(cls, name):
        try:
            return super(cls, cls).find(name)
        except Exception as e:
            default = cls.DEFAULT
            if default is not None:
                return default
            # fi
        # end

        if name is None:
            raise Exception('Could not find a default keychain')
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

# Keychain

class Certificate(Serializable):
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.applications = kwargs.pop('applications', [])
        self.passphrase = kwargs.pop('passphrase', None)
    # __init__

    def serialize(self):
        return {
            "filepath": self.filepath,
            "applications": self.applications,
            "passphrase": self.passphrase
        }
    # serialize
# Cert


class Partition(Serializable):
    def __init__(self, id, **kwargs):
        self.id = id
        self.can_sign = kwargs.pop('can_sign', None)
    # __init__

    def serialize(self):
        return {
            "id": self.id,
            "can_sign": self.can_sign
        }
    # serialize

###
# Utility functions
##

@Keychain.decorator
def create_keychain(name, **kwargs):
    Keychain(name, **kwargs)
# create_keychain

@Keychain.decorator
def default_keychain(name, **kwargs):
    Keychain.find(name).default = True
# default_keychain

@Keychain.decorator
def delete_keychain(name, **kwargs):
    Keychain.delete(name)
# delete_keychain

@Keychain.decorator
def set_keychain_settings(name, **kwargs):
    keychain = Keychain.find(name)
    for k, v in kwargs.items():
        setattr(keychain, k, v)
    # done
# set_keychain_settings

@Keychain.decorator
def unlock_keychain(name, **kwargs):
    Keychain.find(name).unlock(**kwargs)
# unlock_keychain

@Keychain.decorator
def lock_keychain(name, **kwargs):
    Keychain.find(name).lock()
# unlock_keychain

@Keychain.decorator
def import_certificate(name=None, **kwargs):
    Keychain.find(name).import_certificate(**kwargs)
# import_certificate

@Keychain.decorator
def set_key_partition_list(name=None, **kwargs):
    Keychain.find(name).set_partitions(*kwargs.pop('partition_ids', '').split(','), **kwargs)
# set_key_partition_list

if __name__ == '__main__':
    Keychain.load(Keychain.FILE)
    Keychain.status()
# fi

# Keychain
