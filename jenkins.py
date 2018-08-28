#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description="Testing script")
parser.add_argument('--toolchain', help='Toolchain', required=True)
parser.add_argument(
    '--export-file',
    action='store_true',
    help='Use extra file with exports symbols'
)
parser.add_argument(
    '--static',
    action='store_true',
    help='Build static libraries'
)
cmd_args = parser.parse_args()

top_dir = os.getcwd()
install_dir = os.path.join(top_dir, '_install')

def do_call(args, working_dir=top_dir):
  os.chdir(working_dir)
  oneline = ''
  for i in args:
    oneline += ' "{}"'.format(i)
  print('[{}]>{}'.format(os.getcwd(), oneline))
  try:
    subprocess.check_call(args, env=os.environ)
    os.chdir(top_dir)
  except subprocess.CalledProcessError as error:
    print(error)
    print(error.output)
    sys.exit(1)

if os.name == 'nt':
  do_call(['where', 'cmake'])
else:
  do_call(['which', 'cmake'])

do_call(['cmake', '--version'])

do_call([
        'polly.py',
        '--toolchain',
        cmd_args.toolchain,
        '--verbose',
        '--install',
        '--ios-combined',
        '--ios-multiarch',
        '--config',
        'Release',
        '--fwd',
        'CMAKE_CONFIGURATION_TYPES=Release',
        'CMAKE_INSTALL_PREFIX={}'.format(install_dir)
    ],
    working_dir='foo'
)

do_call([
        'polly.py',
        '--toolchain',
        cmd_args.toolchain,
        '--verbose',
        '--install',
        '--ios-combined',
        '--ios-multiarch',
        '--config',
        'Release',
        '--fwd',
        'CMAKE_CONFIGURATION_TYPES=Release',
        'CMAKE_INSTALL_PREFIX={}'.format(install_dir)
    ],
    working_dir='boo'
)

export_file = 'NO'
if cmd_args.export_file:
  export_file = 'YES'

shared_libs = 'YES'
if cmd_args.static:
  shared_libs = 'NO'

do_call([
        'polly.py',
        '--toolchain',
        cmd_args.toolchain,
        '--verbose',
        '--install',
        '--ios-combined',
        '--ios-multiarch',
        '--config',
        'Release',
        '--fwd',
        'CMAKE_CONFIGURATION_TYPES=Release',
        'BUILD_SHARED_LIBS={}'.format(shared_libs),
        'EXPORT_FILE={}'.format(export_file),
        'CMAKE_INSTALL_PREFIX={}'.format(install_dir)
    ],
    working_dir='bar'
)

do_call([
        'polly.py',
        '--toolchain',
        cmd_args.toolchain,
        '--verbose',
        '--config',
        'Release',
        '--fwd',
        'BUILD_SHARED_LIBS={}'.format(shared_libs),
        'CMAKE_CONFIGURATION_TYPES=Release',
        'CMAKE_PREFIX_PATH={}'.format(install_dir)
    ],
    working_dir='baz'
)
