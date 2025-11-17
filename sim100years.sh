#!/bin/bash
for ((i=1; i<=100; i++)); do
	python3 ./offseason.py
	python3 ./league.py
done
