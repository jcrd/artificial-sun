#!/bin/sh

sed "s/@DATETIME/$(date +'%Y, %-m, %-d, %-H, %-M, %-S, 0, 1, -1')/" update.py.in > update.py
cp update.py /run/media/$USER/CIRCUITPY/code.py
rm update.py
sleep 3
cp code.py /run/media/$USER/CIRCUITPY
