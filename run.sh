#!/bin/bash
pipenv run uwsgi config.ini  > /dev/null  &
