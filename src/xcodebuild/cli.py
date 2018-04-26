#!/usr/bin/env python3

import sys
import argparse

from xcodebuild import xcodebuild

parser = argparse.ArgumentParser(description='Mock Xcode Build Utilities')

parser.add_argument('-project',
dest='project', required=True, help='The xcodeproj directory where code is stored')
parser.add_argument('-scheme', dest='scheme', help='The scheme to be used for building')
parser.add_argument('-sdk', dest='sdk', help='The sdk to build for')
parser.add_argument('-destination', dest='destination', help='The platform being built for')
parser.add_argument('-configuration', dest='configuration', help='The configuration for the build which tells the build what to run')
parser.add_argument('vars', nargs='*', help='Extra environment variables to set')
parser.set_defaults(func=xcodebuild)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 1:
        argv = ['--help']
    args = parser.parse_args(argv)
    args.func(**vars(args))
# fi

# xcodebuild.cli
