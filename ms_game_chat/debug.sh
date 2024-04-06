#!/bin/bash

  python3 -m pip install --upgrade pip
  python3 -m pip install django==4.0
  python3 -m pip install channels==4.0.0
  python3 -m pip install daphne==4.0.0
  python3 -m pip install channels_redis
  python3 backend/manage.py makemigrations
  python3 backend/manage.py migrate



# * SETUP DEBUGGER [PYCHARM]

# - add new configuration -> Shell Script
# - choose as script path, path to "debug.sh" script
# - enter working directory: folder in with debug.sh is
# - everything else can be left empty

# - add new configuration -> Python
# - choose as script path to "backend/manage.py"
# - script parameters: runserver 6969
# - click in the top right corner on "modify options" -> "add before launch task"
# - click on "run another configuration" -> choose created shell script

# * before running debugger, make sure you selected the python
#   configuration and not the shell script to debug

# :)
