import argparse
import os
from pathlib import Path

BASEDIR  = str(Path(__file__).parent)
DATA_DIR = os.path.join(BASEDIR, 'data')


global_parser = argparse.ArgumentParser(prog='oxygen')
subparsers    = global_parser.add_subparsers(title='commands')

def build():
    filename = os.path.join(DATA_DIR, 'docs.txt')
    with open(filename, mode='r') as file:
        print(file.read())

def main():
    subparsers.add_parser('build', help='builds the executable file').set_defaults(func=build)

    args = global_parser.parse_args()
    args.func()

