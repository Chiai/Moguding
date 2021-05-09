#!/usr/bin/env python3

from Main import Moguding
import os
import json
import sys

phone_Key = os.environ['Phone']
password_Key = os.environ['Password']
address_Key = os.environ['Address']

try:
    Md = Moguding(phone_Key, password_Key, address_Key)
    Md.run()
    Md.actions
except KeyError:
    print('Plase check username or password.')

