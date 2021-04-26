#!/usr/bin/env python3

import requests
import json
import os
import time
import random
import argparse
import re
import sys
import textwrap

class Moguding():
    def __init__(self, phone, password, address, title, fileName, action=None):
        self.loginUrl = 'https://api.moguding.net:9000/session/user/v1/login'   
        self.saveUrl = 'https://api.moguding.net:9000/attendence/clock/v1/save' 
        self.planUrl = 'https://api.moguding.net:9000/practice/plan/v1/getPlanByStu'    
        self.phone = phone
        self.password = password
        self.address = address
        self.delay = random.randint(0,60)
        self.status = action
        self.title = title
        self.weekReportFile = fileName


    def ServerChan(self, desp):
        SCKEY = "SCU110585Tb6b3e7ef407ea51fe1e43c9cc7b20cb35fe479f1a8d22"
        ServerChanUrl = "http://sc.ftqq.com/" + SCKEY + ".send"
        headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept" : "*/*",
            "Accept-Language" : "*",
            "Accept-Encoding" : "*",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            "text" : self.title,
            "desp" : desp
        }
        requests.post(url=ServerChanUrl,headers=headers,data=data)

    def postUrl(self, url, headers, data):
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

    def sign(self):
        Moguding.getPlanId(self)

        data = {
            'device': 'Android',
            'address': self.address,
            'description': '',
            'country': '',  
            'province': '', 
            'city': '',
            'city': '',
            'longitude': '',
            'latitude': '',
            'planId': Moguding.getPlanId(self),
            'type': self.status
        }
        delay = self.delay
        time.sleep(delay)
        response = Moguding.postUrl(self, url=self.saveUrl, headers=self.headers, data=data)
        response['data'].pop('attendanceId')
        print(f'延迟 {delay}s开始签到.\n{response}')
        if self.status == 'START':
            Moguding.ServerChan(self,desp='账户:'+ self.phone +' 蘑菇丁上班自动签到成功!')
        else:
            Moguding.ServerChan(self,desp='账户:'+ self.phone +' 蘑菇丁下班自动签到成功!')
    
    def WriteWeekReport(self, WeekToWrite, time, LoginToken, PlanID, reportContent):
        WriteReportUrl = 'https://api.moguding.net:9000/practice/paper/v1/save'
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 10; en-us; RMX1901 Build/QKQ1.190918.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization' : LoginToken,
            'rolKey' : 'student',
            'Content-Type' : 'application/json',
            'Accept-Encoding' : 'gzip, deflate'
        }
        data = {
            "reportType":"week",
            "address":self.address,
            "weeks":WeekToWrite,
            "latitude":"0.0",
            "planId":PlanID,
            "startTime":time[0],
            "yearmonth":"",
            "endTime":time[1],
            "title":WeekToWrite + "周报",
            "content":reportContent,
            "longitude":"0.0"
        }
        r = requests.post(url=WriteReportUrl, headers=headers, data=json.dumps(data))
        WriteResult = r.json()
        if WriteResult['code'] == 200:
            WriteReportResult = WriteResult['msg']
            return WriteReportResult
        elif WriteResult['code'] == 500:
            WriteReportResult = WriteResult['msg']
            return WriteReportResult

    def EnumerateWeekReport(self):
        Weeks = ['第1周','第2周','第3周','第4周','第5周','第6周','第7周','第8周','第9周','第10周','第11周','第12周','第13周','第14周','第15周','第16周']
        WeeksReportCalendar = {
            '第1周':['2021-03-01 01:00:00','2021-03-07 23:59:59'],
            '第2周':['2021-03-08 01:00:00','2021-03-14 23:59:59'],
            '第3周':['2021-03-15 01:00:00','2021-03-21 23:59:59'],
            '第4周':['2021-03-22 01:00:00','2021-03-28 23:59:59'],
            '第5周':['2021-03-29 01:00:00','2021-04-04 23:59:59'],
            '第6周':['2021-04-05 01:00:00','2021-04-11 23:59:59'],
            '第7周':['2021-04-12 01:00:00','2021-04-18 23:59:59'],
            '第8周':['2021-04-19 01:00:00','2021-04-25 23:59:59'],
            '第9周':['2021-04-26 01:00:00','2021-05-02 23:59:59'],
            '第10周':['2021-05-03 01:00:00','2021-05-09 23:59:59'],
            '第11周':['2021-05-10 01:00:00','2021-05-16 23:59:59'],
            '第12周':['2021-05-17 01:00:00','2021-05-23 23:59:59'],
            '第13周':['2021-05-24 01:00:00','2021-05-30 23:59:59'],
            '第14周':['2021-05-31 01:00:00','2021-06-06 23:59:59'],
            '第15周':['2021-06-07 01:00:00','2021-06-13 23:59:59'],
            '第16周':['2021-06-14 01:00:00','2021-06-20 23:59:59']
        }
        LoginToken = Moguding.getToken(self)
        PlanID = Moguding.getPlanId(self)
        EnumWeekUrl = 'https://api.moguding.net:9000/practice/paper/v1/listByStu'
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 10; en-us; RMX1901 Build/QKQ1.190918.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization' : LoginToken,
            'rolKey' : 'student',
            'Content-Type' : 'application/json',
            'Accept-Encoding' : 'gzip, deflate'
        }
        data = {
            "reportType":"week",
            #Page Size to int numeric max
            "currPage":"1",
            "pageSize":"2147483647",
            "planId":PlanID
        }
        r = requests.post(url=EnumWeekUrl, headers=headers, data=json.dumps(data))
        EnumResult = r.json()
        CurrentSchedules = []
        if EnumResult['data'] == []:
            desp= "周报检测: \r\n" + "\r\n检测到该同学的所有周报都还没写!" + "\r\n开始撰写第1周周报\r\n"
            f = open(self.weekReportFile,'r')
            reportContenFull = json.loads(f.read())
            reportContent = reportContenFull['第1周']
            WriteReportResult = Moguding.WriteWeekReport(self, WeekToWrite=Weeks[0], time=WeeksReportCalendar[Weeks[0]], LoginToken=LoginToken, PlanID=PlanID, reportContent=reportContent)
            desp = desp + "\r\n\r\n周报撰写结果: " + WriteReportResult + "\r\n\r\n"
            Moguding.ServerChan(self,desp=desp)
        else:
            result = len(EnumResult['data'])
            for i in range(result):
                CurrentSchedules.append(EnumResult['data'][i]['weeks'])
            DifferenceWeeks = [i for i in Weeks if i not in CurrentSchedules]
            if DifferenceWeeks == []:
                desp= "周报检测: \r\n" + " \r\n 全部周报均已完成"
                Moguding.ServerChan(self,desp=desp)
            else:
                desp= "周报检测: \r\n" + "\r\n检测到你还有: " + (",".join(DifferenceWeeks)) + " 的周报没写\r\n" + "\r\n开始撰写" + DifferenceWeeks[0] + "的周报"
                f = open(self.weekReportFile,'r')
                reportContenFull = json.loads(f.read())
                reportContent = reportContenFull[DifferenceWeeks[0]]
                WriteReportResult = Moguding.WriteWeekReport(self, WeekToWrite=DifferenceWeeks[0], time=WeeksReportCalendar[DifferenceWeeks[0]], LoginToken=LoginToken, PlanID=PlanID, reportContent=reportContent)
                desp = desp + "\r\n\r\n周报撰写结果: " + WriteReportResult +"\r\n\r\n"
                Moguding.ServerChan(self,desp=desp)

if __name__=='__main__':
    phone_Key = os.environ['Phone']
    password_Key = os.environ['Password']
    address_Key = os.environ['Address']
    parser = argparse.ArgumentParser(add_help=True, description="This is a script for MoguDing automate sign-in/out and automate write weekly report."
                                    ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-sign", action='store', help='Sign-in/out action, START is for sign-in, END is for sign-out.\n'
                           'usage= "-sign START/END"')
    parser.add_argument("-week", action='store', nargs='?', const=1, help='Weekly report module, usage= "-week"')
    parser.add_argument("-file", action='store', nargs='?', const=1, help='Specify weekly report file, use with "-week" flag, usage= "-file"')

    if len(sys.argv) == 1:
        print(parser.print_help())
        sys.exit(1)
    options = parser.parse_args()
    if sys.argv[1].lstrip('-') == 'sign':
        x = Moguding(phone=phone_Key, password=password_Key, address=address_Key, action=options.sign, title='蘑菇丁自动上下班签到成功!').sign()
    else:
        x = Moguding(phone=phone_Key, password=password_Key, address=address_Key, fileName=options.file, title='蘑菇丁自动写周报').EnumerateWeekReport()
