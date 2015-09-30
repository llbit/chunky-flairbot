#!/bin/bash

set -eu

git pull >/dev/null
python flairbot.py 2>/dev/null
