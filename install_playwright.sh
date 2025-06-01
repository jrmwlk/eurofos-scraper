#!/bin/bash

# Installer les dépendances Python
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Installer les navigateurs Playwright
python3 -m playwright install
