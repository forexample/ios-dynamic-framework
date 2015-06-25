#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description="Testing script")
parser.add_argument('--toolchain', help='Toolchain')
cmd_args = parser.parse_args()

cwd = os.getcwd()

def do_call(args):
  oneline = ''
  for i in args:
    oneline += ' "{}"'.format(i)
  print('[{}]>{}'.format(os.getcwd(), oneline))
  try:
    subprocess.check_call(args, env=os.environ)
  except subprocess.CalledProcessError as error:
    print(error)
    print(error.output)
    sys.exit(1)

if os.path.exists('_install'):
  shutil.rmtree('_install')

if os.path.exists('_3rdParty'):
  shutil.rmtree('_3rdParty')

if os.path.exists('_framework'):
  shutil.rmtree('_framework')

if os.name == 'nt':
  do_call(['where', 'cmake'])
else:
  do_call(['which', 'cmake'])

do_call(['cmake', '--version'])
install_dir = os.path.join('_install')

if os.path.exists('_builds'):
  shutil.rmtree('_builds')

do_call([
    'build.py',
    '--home',
    'Foo',
    '--toolchain',
    cmd_args.toolchain,
    '--verbose',
    '--install',
    '--config',
    'Release'
])

if os.path.exists('_builds'):
  shutil.rmtree('_builds')

do_call([
    'build.py',
    '--home',
    'Boo',
    '--toolchain',
    cmd_args.toolchain,
    '--verbose',
    '--install',
    '--config',
    'Release'
])

shutil.copytree('_install', '_3rdParty')
shutil.rmtree('_install')

if os.path.exists('_builds'):
  shutil.rmtree('_builds')

do_call([
    'build.py',
    '--home',
    'Bar',
    '--toolchain',
    cmd_args.toolchain,
    '--verbose',
    '--framework',
    '--config',
    'Release',
    '--fwd',
    'CMAKE_PREFIX_PATH={}'.format(os.path.join(cwd, '_3rdParty', cmd_args.toolchain))
])

if os.path.exists('_builds'):
  shutil.rmtree('_builds')

do_call([
    'build.py',
    '--home',
    'Baz',
    '--toolchain',
    cmd_args.toolchain,
    '--verbose',
    '--config',
    'Release',
    '--fwd',
    'FRAMEWORK_DIR={}'.format(
        os.path.join(cwd, '_framework', cmd_args.toolchain)
    )
])
