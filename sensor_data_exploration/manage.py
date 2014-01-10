#!/usr/bin/env python

#can anyone see this?
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensor_data_exploration.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
