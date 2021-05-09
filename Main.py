#!/usr/bin/env python3

import requests
import json
import os
import time
import random
import argparse
import sys
from datetime import datetime

class Moguding(object):
    def __init__(self, phone: int, password: str, address: str):
        self.loginUrl = 'https://api.moguding.net:9000/session/user/v1/login'
        self.saveUrl = 'https://api.moguding.net:9000/attendence/clock/v1/save'
        self.planUrl = 'https://api.moguding.net:9000/practice/plan/v1/getPlanByStu'
        self.phone = phone  # 手机号
        self.password = password  #密码
        self.address = address  #签到地点名
        self.delay = random.randint(0, 60)  #延迟时间设置，以s为单位
        self.now = now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def postUrl(self, url: str, headers: dict, data: dict):
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response.json()

    def getToken(self):
        data = {
            'password': self.password,
            'loginType': 'android',
            'uuid': '',
            'phone': self.phone
        }
        response = Moguding.postUrl(self,url=self.loginUrl, headers={'Content-Type': 'application/json; charset=UTF-8',
        'rerfer': 'https://api.moguding.net:9000'}, data=data)
        return response['data']['token']

    def getPlanId(self):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'rerfer': 'https://api.moguding.net:9000',
            'Authorization': Moguding.getToken(self),
            'roleKey': 'student'
        }
        response = Moguding.postUrl(self,url=self.planUrl, headers=self.headers, data={'state': ''})
        return response['data'][0]['planId']

    def stateType(self):
        parser = argparse.ArgumentParser(usage='sign <command> [options]', description='command')
        parser.add_argument('-s', '--sign', choices=['START', 'END'], help='Sign-in/out action, START is for sign-in, END is for sign-out. \n')
        args = parser.parse_args()
        
        if args.sign == None:
            parser.print_help()
            sys.exit(0)

        return args.sign        

    @property
    def actions(self):
        if sys.argv[2] == 'START' or sys.argv[2] == 'END':
            if sys.argv[2] == 'START':
                print(f'{self.now} INFO 上班打卡成功.')
            else:
                print(f'{self.now} INFO 下班打卡成功.')

    def run(self):
        data = {
            'device': 'Android',
            'address': self.address,
            'description': '',  #签到文本
            'country': '',
            'province': '',
            'city': '',
            'city': '',
            'longitude': '',  #经度
            'latitude': '',  #纬度
            'planId': Moguding.getPlanId(self),
            'type': Moguding.stateType(self)
        }

        time.sleep(self.delay)
        response = Moguding.postUrl(self, url=self.saveUrl, headers=self.headers, data=data)
        createTime = response['data']['createTime']
        response.pop('data')

        print(f'{self.now} INFO sleep for {self.delay} seconds ...\n{createTime} INFO {response}')