# Meroshare UI Backend

This project provides a Python-based backend for interacting with the Meroshare API.

## Overview

- Manages first time setup and share application.
- Reads account details from `Acnt.csv` and determines setup flow.
- Allows automatic or manual bank selection based on available banks.

## Usage

1. Update `Acnt.csv` with your account details.
    For initial setup, set the Bank ID to '0'. Once you run main.py, a Bank ID will be provided, which you should then update manually.
2. Run `main.py` to start the application.
3. Follow the on-screen instructions for first time setup or share application.

## Dependencies

- Python 3.x
- requests

 

