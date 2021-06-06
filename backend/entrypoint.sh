#!/bin/sh
celery -A main.celery_app worker -B &
python main.py