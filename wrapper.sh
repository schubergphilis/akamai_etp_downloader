#!/bin/bash
echo 'Python version: '
python --version
[ ! -x ~/.local/bin/pipenv ] && pip install --user pipenv;
~/.local/bin/pipenv install --python 2.7.13
cd $1
~/.local/bin/pipenv run python $2/etp_downloader.py -d $3 -l $4 -s $5 -D --python 2.7.13


