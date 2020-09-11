#!/bin/bash

RUNDIR=/var/opt/akamaietp_downloader
LOGDIR=$RUNDIR/log
LOGFILE=$LOGDIR/akamaietp.log
CSVDIR=$RUNDIR/csv

mkdir -p $LOGDIR
mkdir -p $CSVDIR

python etp_downloader.py -d $CSVDIR -l $LOGFILE -s $ETP_ACCESS_HOST -D
