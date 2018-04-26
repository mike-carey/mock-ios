###
#
##

import os
import abc
import json

from helpers import classproperty

class Serializable(object, metaclass=abc.ABCMeta):
    INVENTORY = {}

    @classproperty
    def FILE(cls):
        return os.environ.get(cls.ENVIRONMENT_VARIABLE, cls.DEFAULT_FILE)
    # FILE

    @classproperty
    def DEFAULT_FILE(cls):
        return './%s.json' % cls.__name__.lower()
    # DEFAULT_FILE

    @classproperty
    def ENVIRONMENT_VARIABLE(cls):
        return '%s_FILE' % cls.__name__.upper()
    # ENVIRONMENT_VARIABLE

    @classproperty
    def JSON_KEY(cls):
        return None
    # JSON_KEY

    @abc.abstractmethod
    def serialize(self):
        raise NotImplementedError('Please define the serialize function')
    # serialize

    @classmethod
    def deserialize(cls, **kwargs):
        return cls(**kwargs)
    # deserialize

    @classmethod
    def load(cls, filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = {}
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    print("Could not decode json for %s.  Moving on" % filename)
                # end
            # end

            if cls.JSON_KEY is not None:
                data = data.get(cls.JSON_KEY, {})
            # fi

            for key, val in data.items():
                cls.INVENTORY[key] = cls.deserialize(**val)
            # done
        # fi
    # load

    @classmethod
    def save(cls, filename):
        data = {}
        for key, val in cls.INVENTORY.items():
            data[key] = val.serialize()
        # done

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump({
                cls.JSON_KEY: data
            }, f, indent=2)
        # end
    # save

    @classmethod
    def find(cls, name):
        if name not in cls.INVENTORY:
            raise Error('Could not find %s' % name)
        # fi

        return cls.INVENTORY[name]
    # find

    @classmethod
    def delete(cls, name):
        if name not in cls.INVENTORY:
            raise Exception('Could not find %s' % name)
        # fi

        del cls.INVENTORY[name]
    # delete

    @classmethod
    def status(cls):
        obj = {}
        for key, val in cls.INVENTORY.items():
            obj[key] = val.serialize()
        # done

        print(json.dumps(obj))
    # status

    @classmethod
    def add(cls, name, obj):
        cls.INVENTORY[name] = obj
    # add

    @classmethod
    def decorator(cls, fn):
        def _decorator(*args, **kwargs):
            cls.load(cls.FILE)
            value = fn(*args, **kwargs)
            cls.save(cls.FILE)

            return value
        # _decorator

        return _decorator
    # decorator

# Serializable

# serialize
