#!/bin/sh
# Install dependencies
pip install -r requirements.txt
lsb_release -i
apt install docker