#! /usr/bin/env bash

perl -p -e 's/-[0-9]*(\.|e-)[0-9]*/0/g' $1 | head -n 1

