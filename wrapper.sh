#!/bin/bash
[ ! -x ~/.local/bin/pipenv ] && pip install --user pipenv > /dev/null 2>&1;
~/.local/bin/pipenv install > /dev/null 2>&1;
~/.local/bin/pipenv run python $1/etp_downloader.py -d $2 -l $3 -s $4 -D
