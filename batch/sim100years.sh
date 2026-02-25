#!/bin/bash
for ((i=1; i<=100; i++)); do
	python3 ../src/offseason.py
	python3 ../src/league.py
done
