#!/bin/bash
[ ! -x ~/.local/bin/pipenv ] && pip install --user pipenv;
~/.local/bin/pipenv install
~/.local/bin/pipenv run python $1/etp_downloader.py -d $2 -l $3 -s $4 -D
