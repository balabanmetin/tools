#! /usr/bin/env bash

comm -12 <(nw_labels -I $1 | sort ) <(nw_labels -I $2 | sort) > .common
quartet_dist -v <(nw_prune -v $1 `cat .common`) <(nw_prune -v $2 `cat .common`) | cut -f4
rm .common
