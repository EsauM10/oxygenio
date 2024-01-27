import argparse
import json
import os
from pathlib import Path

from oxygenio.helpers import create_file, read_file

BASEDIR  = str(Path(__file__).parent)
DATA_DIR = os.path.join(BASEDIR, 'data')


global_parser = argparse.ArgumentParser(prog='oxygen')
subparsers    = global_parser.add_subparsers(title='commands')

def build():
    filename = os.path.join(DATA_DIR, 'docs.txt')
    with open(filename, mode='r') as file:
        print(file.read())

def create():
    data = {
        'devCommand': 'npm run dev',
        'buildCommand': 'npm run build',
        'appURL': 'http://localhost:5173',
        'distFolder': 'dist'
    }
    print('Creating config.json 📂...')
    create_file('config.json', json.dumps(data, indent=4))

    print('Creating main.py 📄...')
    sample_file = os.path.join(DATA_DIR, 'sample.txt')
    create_file('main.py', read_file(sample_file))
    
    

def main():
    subparsers.add_parser('build', help='builds the executable file').set_defaults(func=build)
    subparsers.add_parser('create', help='create all the necessaries files').set_defaults(func=create)
    
    args = global_parser.parse_args()
    args.func()

