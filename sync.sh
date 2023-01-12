#!/bin/sh

cp code.py /run/media/$USER/CIRCUITPY

while inotifywait -e modify code.py; do
	cp code.py /run/media/$USER/CIRCUITPY
done
