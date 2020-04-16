#!/usr/bin/env bash

# $1 fasta file

sed '/^>/!s/\(..\)./\1-/g' $1
