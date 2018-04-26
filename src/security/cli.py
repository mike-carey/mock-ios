#!/usr/bin/env python3

import sys
import argparse
from keychain import create_keychain, delete_keychain, default_keychain, set_keychain_settings, unlock_keychain, lock_keychain, import_certificate

parser = argparse.ArgumentParser(description='Mock security')
subparsers = parser.add_subparsers(help='sub-command help')

create_keychain_parser = subparsers.add_parser('create-keychain', help='Creates a keychain')
create_keychain_parser.add_argument('-p',
dest='password', help='The password for the keychain')
create_keychain_parser.add_argument('name', help='The keychain to create')
create_keychain_parser.set_defaults(func=create_keychain)

delete_keychain_parser = subparsers.add_parser('delete-keychain', help='Deletes a keychain')
delete_keychain_parser.add_argument('-p', dest='password', help='The password for the keychain')
delete_keychain_parser.add_argument('name', help='The keychain to delete')
delete_keychain_parser.set_defaults(func=delete_keychain)

default_keychain_parser = subparsers.add_parser('default-keychain', help='Sets the default keychain')
default_keychain_parser.add_argument('-s', dest='name', help='The password for the keychain')
default_keychain_parser.set_defaults(func=default_keychain)

unlock_keychain_parser = subparsers.add_parser('unlock-keychain', help='Unlocks the keychain')
unlock_keychain_parser.add_argument('-p', dest='password', help='The password for the keychain')
unlock_keychain_parser.add_argument('name', help='The keychain to unlock')
unlock_keychain_parser.set_defaults(func=unlock_keychain)

lock_keychain_parser = subparsers.add_parser('lock-keychain', help='Locks the keychain')
lock_keychain_parser.add_argument('name', help='The keychain to unlock')
lock_keychain_parser.set_defaults(func=lock_keychain)

set_keychain_settings_parser = subparsers.add_parser('set-keychain-settings', help='Sets keychain settings')
set_keychain_settings_parser.add_argument('-t', dest='timeout', help='The timeout for the keychain')
set_keychain_settings_parser.add_argument('-l', dest='lock_on_sleep', action='store_true', help='Lock keychain when the system sleeps')
set_keychain_settings_parser.add_argument('name', help='The keychain location')
set_keychain_settings_parser.set_defaults(func=set_keychain_settings)

import_parser = subparsers.add_parser('import', help='Imports a secret')
import_parser.add_argument('-k', dest='name', help='The key chain to add this secret to')
import_parser.add_argument('-P', dest='passphrase', help='The passphrase for the secret')
import_parser.add_argument('-T', dest='applications', nargs='*', help='The applications that are allowed to use the certificate')
import_parser.add_argument('filepath', help='The certificate location')
import_parser.set_defaults(func=import_certificate)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 1:
        argv = ['--help']
    args = parser.parse_args(argv)
    args.func(**vars(args))
# fi

# security.cli
