#!/bin/bash
[ ! -x ~/.local/bin/pipenv ] && pip install --user pipenv;
scl enable python27 '~/.local/bin/pipenv install'
cd $1
scl enable python27 '~/.local/bin/pipenv run python $2/etp_downloader.py -d $3 -l $4 -s $5 -D'


