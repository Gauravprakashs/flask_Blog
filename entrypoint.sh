#!/bin/bash
flask db upgrade
exec python app.py