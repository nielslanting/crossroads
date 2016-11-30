# This module runs all *_test.py files in the current directory

import subprocess
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
command = 'python -m unittest discover -s ' + dir_path + ' -p \'*_test.py\''
subprocess.Popen(command, shell=True)
