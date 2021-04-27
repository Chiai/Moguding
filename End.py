#!/usr/bin/env python3

from Main import Moguding as Md
import os

phone_Key = os.environ['Phone']
password_Key = os.environ['Password']
address_Key = os.environ['Address']

Md(phone_Key, password_Key, address_Key, 'START').run()