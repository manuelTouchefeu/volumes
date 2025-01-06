#!/bin/bash
gunicorn --config config.py volumes:application
