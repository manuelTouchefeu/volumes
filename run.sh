#!/bin/bash
source volumenv/bin/activate
gunicorn --config config.py volumes:application
