#!/bin/sh
while true; do
    python recursive_art.py
    $? && break
done
