#!/usr/bin/env python3

import requests
import json
import os
import time
import random

class Moguding():
    def __init__(self,phone,password,address,stateType):
        self.loginUrl = 'https://api.moguding.net:9000/session/user/v1/login'   
        self.saveUrl = 'https://api.moguding.net:9000/attendence/clock/v1/save' 
        self.planUrl = 'https://api.moguding.net:9000/practice/plan/v1/getPlanByStu'    
        self.phone = phone  # 手机号
        self.password = password    #密码
        self.address = address  #签到地点名
        self.delay = random.randint(0,60) #延迟时间设置，以s为单位
        self.stateType = stateType #START 上班 END 下班

    def postUrl(self,url,headers,data):
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response.json()

    def getToken(self):
        data ={
            'password': self.password,
            'loginType': 'android',
            'uuid': '',
            'phone': self.phone
        }
        response = Moguding.postUrl(self, url =self.loginUrl,headers={'Content-Type': 'application/json; charset=UTF-8',
            'rerfer': 'https://api.moguding.net:9000'},data=data)
        return response['data']['token']

    def getPlanId(self):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'rerfer': 'https://api.moguding.net:9000',
            'Authorization': Moguding.getToken(self),
            'roleKey': 'student'
        }

        data = {'state':''}
        response = Moguding.postUrl(self, url =self.planUrl,headers =self.headers,data=data)
        return response['data'][0]['planId']

    def run(self):
        Moguding.getPlanId(self)

        data = {
            'device': 'Android',
            'address': self.address,
            'description': '',  #签到文本
            'country': '',  
            'province': '', 
            'city': '',
            'city': '',
            'longitude': '',    #经度
            'latitude': '', #纬度
            'planId': Moguding.getPlanId(self),
            'type': self.stateType 
        }

        delay = self.delay
        time.sleep(delay)
        response = Moguding.postUrl(self, url =self.saveUrl, headers =self.headers,data=data)
        response['data'].pop('attendanceId')
        print(f'延迟 {delay}s开始签到.\n{response}')