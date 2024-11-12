import argparse
import json
import os

from oxygenio.build import ViteBuilder
from oxygenio.config import ConfigLoader
from oxygenio.helpers import (
    CONFIG_FILENAME, DATA_DIR, 
    create_file, read_file
)

global_parser = argparse.ArgumentParser(prog='oxygen')
subparsers    = global_parser.add_subparsers(title='commands')

def build():
    config = ConfigLoader()
    ViteBuilder(config).build()

def init():
    data = {
        'mode': 'dev',
        'appURL': 'http://localhost:5173',
        'devCommand': 'npm --prefix=web run dev',
        'buildCommand': 'npm --prefix=web run build',
        'frontendApp': 'web',
        'distFolder': 'dist',
        'staticFolder': 'assets'
    }
    print(f'Creating {CONFIG_FILENAME} 📂...')
    create_file(CONFIG_FILENAME, json.dumps(data, indent=4))

    print('Creating main.py 📄...')
    sample_file = os.path.join(DATA_DIR, 'sample.txt')
    create_file('main.py', read_file(sample_file))
    
    

def main():
    subparsers.add_parser('build', help='builds the executable file').set_defaults(func=build)
    subparsers.add_parser('init', help='initialize a new oxygen project').set_defaults(func=init)
    
    args = global_parser.parse_args()
    args.func()

