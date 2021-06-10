#!/usr/bin/env bash

FILEID=$1
FILENAME=$2

x=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$FILEID" -O- | sed -rn "s/.*confirm=([1-9A-Za-z_]+).*/\1\n/p")

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=${x}&id=$FILEID" -O $FILENAME && rm -rf /tmp/cookies.txt
